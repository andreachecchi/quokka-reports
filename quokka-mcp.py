"""
MCP Server for automatic dataset publishing.

This server automatically discovers and publishes all datasets from the configuration,
regardless of their data provider (postgresql, graylog, etc.).
"""

import asyncio
import json
import os
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
import pandas as pd
import importlib.util
from datetime import datetime
from functools import wraps

def require_auth(func):
    """Decorator to require authentication via MCP_AUTH_TOKEN.

    In FastMCP 3.x la Request HTTP non viene passata alle callable dei tool:
    va letta dal contextvar di richiesta tramite get_http_headers().
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        from fastmcp.server.dependencies import get_http_headers

        # get_http_headers non solleva mai eccezioni: dict vuoto se non c'e'
        # una richiesta HTTP attiva (es. trasporto stdio).
        try:
            headers = get_http_headers(include={"authorization"})
        except Exception:
            headers = {}

        auth_header = headers.get("authorization", "")

        # Check if token is valid
        if not auth_header or not auth_header.startswith('Bearer '):
            return json.dumps({"error": "Authentication required. Please provide a valid Bearer token."})

        token = auth_header[7:]  # Remove 'Bearer ' prefix

        # Load config and verify token
        try:
            from config import MCP_AUTH_TOKEN
            if token != MCP_AUTH_TOKEN:
                return json.dumps({"error": "Invalid authentication token."})
        except ImportError:
            return json.dumps({"error": "Authentication server configuration not found."})

        # Call the original function
        return func(*args, **kwargs)
    return wrapper


# Create MCP server instance
mcp = FastMCP("dataset-server")


def _load_provider_function(provider_type):
    """
    Dynamically load a provider function from data_providers directory.
    """
    providers_dir = Path('data_providers')
    provider_file = providers_dir / f"{provider_type}.py"
    
    spec = importlib.util.spec_from_file_location(f"provider_{provider_type}", provider_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module.fetch_data


def _discover_datasets():
    """Discover all datasets from the datasets directory."""
    datasets_dir = Path('datasets')
    datasets = []
    
    if not datasets_dir.exists():
        return datasets
    
    for ds_dir in datasets_dir.iterdir():
        if ds_dir.is_dir():
            ds_json_path = ds_dir / 'dataset.json'
            if ds_json_path.exists():
                try:
                    with open(ds_json_path, 'r') as f:
                        ds_config = json.load(f)
                    
                    dataset_id = ds_config.get('id')
                    if dataset_id:
                        datasets.append({
                            'id': dataset_id,
                            'name': ds_config.get('name', dataset_id),
                            'description': ds_config.get('description', ''),
                            'provider': ds_config.get('database', {}).get('type', 'unknown'),
                            'directory': str(ds_dir),
                            'config': ds_config
                        })
                except Exception as e:
                    mcp.log.error(f"Error loading dataset from {ds_dir}: {e}")
    
    return datasets


def _fetch_data(dataset_config, dataset_dir):
    """Fetch data from database using dataset configuration."""
    provider_type = dataset_config.get('database', {}).get('type', 'postgresql')
    fetch_function = _load_provider_function(provider_type)
    return fetch_function(dataset_config, dataset_dir)


@mcp.tool()
@require_auth
def list_datasets() -> str:
    """List all available datasets with their configuration."""
    datasets = _discover_datasets()
    return json.dumps(datasets, indent=2, default=str)


@mcp.tool()
@require_auth
def get_dataset_config(dataset_id: str) -> str:
    """Get detailed configuration for a specific dataset by ID."""
    datasets = _discover_datasets()
    for ds in datasets:
        if ds['id'] == dataset_id:
            return json.dumps(ds, indent=2, default=str)
    return json.dumps({"error": f"Dataset '{dataset_id}' not found"})


@mcp.tool()
@require_auth
def fetch_dataset_data(dataset_id: str, params: str = "{}") -> str:
    """Fetch data from a specific dataset by ID with optional parameters.
    
    Args:
        dataset_id: The ID of the dataset to fetch
        params: JSON string of parameters (e.g., '{"from_date": "2026-01-01", "to_date": "2026-12-31"}')
    
    Returns:
        Dataset data as JSON with columns and rows
    """
    datasets = _discover_datasets()
    dataset_info = None
    
    for ds in datasets:
        if ds['id'] == dataset_id:
            dataset_info = ds
            break
    
    if not dataset_info:
        return json.dumps({"error": f"Dataset '{dataset_id}' not found"})
    
    try:
        param_dict = json.loads(params) if params else {}
        dataset_config = dataset_info['config'].copy()
        dataset_config['_params'] = param_dict
        
        data = _fetch_data(dataset_config, Path(dataset_info['directory']))
        
        # Convert numpy types to Python native types for JSON serialization
        result = {
            'columns': data['columns'],
            'rows': []
        }
        
        for row in data['rows']:
            converted_row = []
            for cell in row:
                if isinstance(cell, (pd.Series, pd.DataFrame)):
                    converted_row.append(str(cell))
                elif hasattr(cell, 'item'):  # numpy types
                    converted_row.append(cell.item())
                elif isinstance(cell, datetime):
                    converted_row.append(cell.isoformat())
                else:
                    converted_row.append(cell)
            result['rows'].append(converted_row)
        
        return json.dumps(result, indent=2, default=str)
    
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch data: {str(e)}"})


@mcp.tool()
@require_auth
def generate_dataset_report(dataset_id: str, report_id: str, params: str = "{}") -> str:
    """Generate a report for a specific dataset.
    
    Args:
        dataset_id: The ID of the dataset to generate report for
        report_id: The ID of the report template to use
        params: JSON string of parameters (e.g., '{"from_date": "2026-01-01"}')
    
    Returns:
        Path to the generated report file
    """
    from engine import generate_report
    
    try:
        param_dict = json.loads(params) if params else {}
        
        report_params = []
        if param_dict:
            report_params.append({
                'dataset_id': dataset_id,
                'params': [{k: v} for k, v in param_dict.items()]
            })
        
        output_path = generate_report(report_id, report_params)
        return json.dumps({"success": True, "path": str(output_path)}, indent=2)
    
    except Exception as e:
        return json.dumps({"error": f"Failed to generate report: {str(e)}"})


@mcp.tool()
@require_auth
def get_dataset_summary(dataset_id: str, params: str = "{}") -> str:
    """Get a summary of a dataset including row count and column info.
    
    Args:
        dataset_id: The ID of the dataset
        params: JSON string of parameters
    
    Returns:
        Summary information as JSON
    """
    try:
        data_json = fetch_dataset_data(dataset_id, params)
        data = json.loads(data_json)
        
        if 'error' in data:
            return data_json
        
        summary = {
            'dataset_id': dataset_id,
            'row_count': len(data['rows']),
            'column_count': len(data['columns']),
            'columns': data['columns']
        }
        
        # Try to get basic statistics for numeric columns
        if data['rows']:
            df = pd.DataFrame(data['rows'], columns=data['columns'])
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols:
                summary['numeric_columns_stats'] = {}
                for col in numeric_cols:
                    summary['numeric_columns_stats'][col] = {
                        'min': float(df[col].min()) if not pd.isna(df[col].min()) else None,
                        'max': float(df[col].max()) if not pd.isna(df[col].max()) else None,
                        'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                        'null_count': int(df[col].isna().sum())
                    }
        
        return json.dumps(summary, indent=2, default=str)
    
    except Exception as e:
        return json.dumps({"error": f"Failed to generate summary: {str(e)}"})


if __name__ == "__main__":
    # Run the MCP server with streamable-http transport
    from config import MCP_HOST, MCP_PORT, MCP_AUTH_TOKEN

    mcp.run(transport="streamable-http", host=MCP_HOST, port=MCP_PORT)
