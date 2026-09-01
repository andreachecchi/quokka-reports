# report scheduler here
#
#


import datetime
import json
import os
import zipfile
import shutil
from engine import generate_excel_report


def get_previous_day_date_range():
    """Get the date range for the previous day.
    
    Returns:
        tuple: (from_date, to_date) as strings in ISO format "YYYY-MM-DDTHH:MM:SS.000Z"
    """
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    # Format for Graylog: ISO 8601 with milliseconds
    from_date = yesterday.strftime('%Y-%m-%dT%H:%M:00.000Z')
    to_date = today.strftime('%Y-%m-%dT%H:%M:00.000Z')
    
    return from_date, to_date


def schedule_reports():
    """Schedule and run Excel report generation for configured reports."""
    # Get the previous day's date range
    from_date, to_date = get_previous_day_date_range()
    
    # Define reports to schedule
    reports_to_run = ['sample_v1', 'sample_v2']
    
    print(f"Running scheduled reports with date range: {from_date} to {to_date}")
    
    # List to store generated file paths
    generated_files = []
    
    for report_id in reports_to_run:
        try:
            print(f"\n" + "="*60)
            print(f"Processing report: {report_id}")
            print(f"="*60)
            
            # Read the report configuration to get dataset IDs
            report_config_path = os.path.join('reports', f'{report_id}.rp', 'report.json')
            print(f"Loading report configuration from: {report_config_path}")
            with open(report_config_path, 'r') as f:
                report_config = json.load(f)
            
            # Extract dataset IDs from the report configuration
            dataset_ids = [ds['id'] for ds in report_config.get('datasets', [])]
            
            print(f"Report name: {report_config.get('name', 'N/A')}")
            print(f"Report category: {report_config.get('category', 'N/A')}")
            print(f"Report tags: {', '.join(report_config.get('tags', []))}")
            print(f"Number of datasets: {len(dataset_ids)}")
            print(f"Dataset IDs: {', '.join(dataset_ids)}")
            
            # Build params with all datasets from the report
            params = {
                report_id: {
                    'from': from_date,
                    'to': to_date
                }
            }
            
            # Add dataset parameters for each dataset in the report
            for dataset_id in dataset_ids:
                params[dataset_id] = {
                    'from': from_date,
                    'to': to_date
                }
                print(f"Added dataset parameter: {dataset_id} (from: {from_date}, to: {to_date})")
            
            print(f"Generating Excel report with {len(dataset_ids)} dataset(s)...")
            
            # Generate Excel report
            output_path = generate_excel_report(report_id, params)
            print(f"\n✓ Excel report generated successfully: {output_path}")
            
            # Track generated file
            generated_files.append(output_path)
            
        except FileNotFoundError as e:
            print(f"\n✗ Error: Report or dataset not found for {report_id}: {e}")
        except Exception as e:
            print(f"\n✗ Error generating report {report_id}: {e}")
    
    # Create zip archive with from_date in filename
    if generated_files:
        # Extract date part from from_date (ISO format: YYYY-MM-DDTHH:MM:SS.000Z)
        # Convert to YYYY-MM-DD_HH-MM for filename
        from_date_filename = from_date.replace('T', '_').replace(':', '-').split('.')[0]
        zip_filename = f"reports_{from_date_filename}.zip"
        
        # Create zip archive
        zip_path = os.path.join('generated', zip_filename)
        print(f"\n" + "="*60)
        print(f"Creating zip archive: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in generated_files:
                if os.path.exists(file_path):
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")
        
        print(f"✓ Zip archive created successfully: {zip_path}")
        
        # Delete original files after adding to zip
        print("\nDeleting original files...")
        for file_path in generated_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"  Deleted: {os.path.basename(file_path)}")


if __name__ == '__main__':
    schedule_reports()
