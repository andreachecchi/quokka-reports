import os
import json
import re
import datetime
import psycopg2
import shutil
import importlib.util
from pathlib import Path


def _load_provider_function(provider_type):
    """
    Dynamically load a provider function from data_providers directory.
    
    Args:
        provider_type: String with the provider type (e.g., 'postgresql', 'sqlite')
    
    Returns:
        The fetch_data function from the provider module
    """
    providers_dir = Path('data_providers')
    provider_file = providers_dir / f"{provider_type}.py"
    
    spec = importlib.util.spec_from_file_location(f"provider_{provider_type}", provider_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module.fetch_data

def _fetch_data(dataset_config, dataset_dir):
    """Fetch data from database using dataset configuration."""
    provider_type = dataset_config['database'].get('type', 'postgresql')
    fetch_function = _load_provider_function(provider_type)
    
    return fetch_function(dataset_config, dataset_dir)

def _render_template(template_content, dataset_results, report_config):
    """Render the HTML template with dataset results."""

    html = template_content

    for dataset_id, data in dataset_results.items():

        print(dataset_id)

        tbody_content = ''

        for row in data['rows']:
            tbody_content += '\n          '

            for cell in row:
                tbody_content += f'{cell}'

            tbody_content += ''

        target_id = f'data-id="{dataset_id}"'

        if target_id in html:
            html = re.sub(
                rf'(<tbody[^>]*{re.escape(target_id)}[^>]*>\s*)(\s*</tbody>)',
                lambda m: m.group(1) + tbody_content + m.group(2),
                html,
                count=1
            )

        elif '<tbody>' in html:
            html = re.sub(
                r'(<tbody>\s*)(\s*</tbody>)',
                lambda m: m.group(1) + tbody_content + m.group(2),
                html,
                count=1
            )

    return html

def _extract_resources_from_html(html_content, base_path):
    """Extract resource references (css, js, images) from HTML content.
    
    Args:
        html_content: HTML content as string
        base_path: Base directory path to resolve relative URLs
    
    Returns:
        Set of resource file paths to copy
    """
    resources = set()
    
    # Match href and src attributes
    patterns = [
        r'href=["\']([^"\']+)["\']',  # href links (CSS, anchors)
        r'src=["\']([^"\']+)["\']',    # src attributes (images, scripts)
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            # Skip data: URLs and javascript: URLs
            if match.startswith('data:') or match.startswith('javascript:'):
                continue
            
            # Convert to Path and check if it's a relative file reference
            resource_path = Path(match)
            
            # Skip absolute URLs (http://, https://)
            if resource_path.parts[0].startswith(('http://', 'https://')):
                continue
            
            # Skip anchor links
            if resource_path.parts[0].startswith('#'):
                continue
            
            # Try to resolve the path relative to base_path
            resolved_path = base_path / resource_path
            if resolved_path.exists():
                resources.add(str(resolved_path))
    
    return resources


def _copy_resources_to_generated(html_content, resources, report_dir, generated_dir):
    """Copy resource files to generated directory and update HTML paths.
    
    Args:
        html_content: Original HTML content
        resources: List of resource file paths to copy
        report_dir: Source report directory
        generated_dir: Destination generated directory
    
    Returns:
        Updated HTML content with corrected paths
    """
    import shutil
    
    # Create subdirectory structure if needed
    generated_dir.mkdir(parents=True, exist_ok=True)
    
    updated_content = html_content
    
    for resource_path_str in resources:
        resource_path = Path(resource_path_str)
        
        if not resource_path.exists():
            continue
        
        # Determine destination path (keep relative structure)
        dest_path = generated_dir / resource_path.relative_to(report_dir)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(resource_path, dest_path)
        
        # Update paths in HTML content
        # Get the relative path from generated HTML to the copied resource
        html_to_resource = os.path.relpath(dest_path, generated_dir)
        
        # Replace in HTML - handle both single and double quotes
        old_path_str = str(resource_path.relative_to(report_dir))
        updated_content = updated_content.replace(f'href="{old_path_str}"', f'href="{html_to_resource}"')
        updated_content = updated_content.replace(f"href='{old_path_str}'", f"href='{html_to_resource}'")
        updated_content = updated_content.replace(f'src="{old_path_str}"', f'src="{html_to_resource}"')
        updated_content = updated_content.replace(f"src='{old_path_str}'", f"src='{html_to_resource}'")
    
    return updated_content


def generate_report(report_id, params):
    """Generate a report with the given ID and parameters.
    
    Args:
        report_id: The ID of the report to generate (from report.json)
        params: List of parameter objects, e.g., [
            {"dataset_id": "sample_dataset_v1", "params": [{"from_date": "2026-01-01"}]}
        ]
    
    Returns:
        Path to the generated HTML file
    """
    # Discover and find report directory by matching ID in report.json
    reports_dir = Path('reports')
    report_dir = None
    if reports_dir.exists():
        for rp_dir in reports_dir.iterdir():
            if rp_dir.is_dir():
                report_json_path = rp_dir / 'report.json'
                if report_json_path.exists():
                    try:
                        with open(report_json_path, 'r') as f:
                            report_config = json.load(f)
                        # Match by the 'id' field in report.json
                        if report_config.get('id') == report_id:
                            report_dir = rp_dir
                            break
                    except:
                        continue
    
    if not report_dir:
        raise FileNotFoundError(f"Report directory not found for ID: {report_id}")
    
    # Read report configuration
    report_config_path = report_dir / 'report.json'
    if not report_config_path.exists():
        raise FileNotFoundError(f"Report config not found: {report_config_path}")
    
    with open(report_config_path, 'r') as f:
        report_config = json.load(f)
    
    # Read template files
    template_path = report_dir / report_config.get('template', 'report.html')
    style_path = report_dir / report_config.get('style', 'report.css')
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    with open(style_path, 'r') as f:
        style_content = f.read()
    
    # Add main style CSS as inline style in head if not already present
    style_tag = f'<style>{style_content}</style>'
    if '<style>' not in template_content:
        template_content = template_content.replace('</head>', f'    {style_tag}\n</head>')
    
    # Extract additional resources (images, other CSS/JS) from HTML
    resource_files = _extract_resources_from_html(template_content, report_dir)
    
    # Build dataset param mapping: dataset_id -> dict of parameters
    dataset_params_map = {}
    for param_group in params:
        dataset_id = param_group.get('dataset_id')
        if dataset_id and 'params' in param_group:
            # Convert list of single-key dicts to single dict
            param_dict = {}
            for p in param_group['params']:
                for key, value in p.items():
                    param_dict[key] = value
            dataset_params_map[dataset_id] = param_dict
    
    # Get datasets from report config and discover them
    datasets = report_config.get('datasets', [])
    dataset_results = {}
    
    datasets_dir = Path('datasets')
    for dataset_config in datasets:
        dataset_id = dataset_config.get('id')
        if not dataset_id:
            continue
        
        # Discover dataset directory and match by dataset.json id field
        dataset_dir = None
        if datasets_dir.exists():
            for ds_dir in datasets_dir.iterdir():
                if ds_dir.is_dir():
                    ds_json_path = ds_dir / 'dataset.json'
                    if ds_json_path.exists():
                        try:
                            with open(ds_json_path, 'r') as f:
                                ds_config = json.load(f)
                            if ds_config.get('id') == dataset_id:
                                dataset_dir = ds_dir
                                break
                        except:
                            continue
        
        if not dataset_dir:
            raise FileNotFoundError(f"Dataset directory not found for id: {dataset_id}")
        
        dataset_json_path = dataset_dir / 'dataset.json'
        if not dataset_json_path.exists():
            raise FileNotFoundError(f"Dataset config not found: {dataset_json_path}")
        
        with open(dataset_json_path, 'r') as f:
            full_dataset_config = json.load(f)
        
        # Add parameters to dataset config (if available for this dataset)
        if dataset_id in dataset_params_map:
            full_dataset_config['_params'] = dataset_params_map[dataset_id]
        else:
            full_dataset_config['_params'] = {}
        
        # Fetch data
        data = _fetch_data(full_dataset_config, dataset_dir)
        dataset_results[dataset_id] = data
    
    # Render template with data
    rendered_html = _render_template(template_content, dataset_results, report_config)
    
    # Create generated output directory
    generated_dir = Path('generated')
    generated_dir.mkdir(exist_ok=True)
    
    # Copy additional resources (images, CSS, JS) to generated directory
    for resource_path_str in resource_files:
        resource_path = Path(resource_path_str)
        if resource_path.exists():
            dest_path = generated_dir / resource_path.relative_to(report_dir)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resource_path, dest_path)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    output_filename = f"{report_id}_{timestamp}.html"
    output_path = generated_dir / output_filename
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(rendered_html)
    
    return output_path


def generate_excel_report(report_id: str, params: dict) -> str:
    """
    Generate an Excel file with multiple sheets (one per dataset) for the given report.
    
    Args:
        report_id: The ID of the report to generate
        params: Dictionary mapping dataset_id -> dict of parameters
        
    Returns:
        Path to the generated Excel file
    """
    # Discover and find report directory by matching ID in report.json
    reports_dir = Path('reports')
    report_dir = None
    if reports_dir.exists():
        for rp_dir in reports_dir.iterdir():
            if rp_dir.is_dir():
                report_json_path = rp_dir / 'report.json'
                if report_json_path.exists():
                    try:
                        with open(report_json_path, 'r') as f:
                            report_config = json.load(f)
                        # Match by the 'id' field in report.json
                        if report_config.get('id') == report_id:
                            report_dir = rp_dir
                            break
                    except:
                        continue
    
    if not report_dir:
        raise FileNotFoundError(f"Report directory not found for ID: {report_id}")
    
    # Read report configuration
    report_config_path = report_dir / 'report.json'
    if not report_config_path.exists():
        raise FileNotFoundError(f"Report config not found: {report_config_path}")
    
    with open(report_config_path, 'r') as f:
        report_config = json.load(f)
    
    # Get datasets from report config and discover them
    datasets = report_config.get('datasets', [])
    dataset_results = {}
    
    datasets_dir = Path('datasets')
    for dataset_config in datasets:
        dataset_id = dataset_config.get('id')
        if not dataset_id:
            continue
        
        # Discover dataset directory and match by dataset.json id field
        dataset_dir = None
        if datasets_dir.exists():
            for ds_dir in datasets_dir.iterdir():
                if ds_dir.is_dir():
                    ds_json_path = ds_dir / 'dataset.json'
                    if ds_json_path.exists():
                        try:
                            with open(ds_json_path, 'r') as f:
                                ds_config = json.load(f)
                            if ds_config.get('id') == dataset_id:
                                dataset_dir = ds_dir
                                break
                        except:
                            continue
        
        if not dataset_dir:
            raise FileNotFoundError(f"Dataset directory not found for id: {dataset_id}")
        
        dataset_json_path = dataset_dir / 'dataset.json'
        if not dataset_json_path.exists():
            raise FileNotFoundError(f"Dataset config not found: {dataset_json_path}")
        
        with open(dataset_json_path, 'r') as f:
            full_dataset_config = json.load(f)
        
        # Add parameters to dataset config (if available for this dataset)
        if dataset_id in params:
            full_dataset_config['_params'] = params[dataset_id]
        else:
            full_dataset_config['_params'] = {}
        
        # Fetch data
        data = _fetch_data(full_dataset_config, dataset_dir)
        dataset_results[dataset_id] = data
    
    # Create generated output directory
    generated_dir = Path('generated')
    generated_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    output_filename = f"{report_id}_{timestamp}.xlsx"
    output_path = generated_dir / output_filename
    
    # Import and use excel module
    from excel import generate_excel
    excel_path = generate_excel(dataset_results, str(output_path))
    
    return excel_path
