# report scheduler here
#
#


import datetime
import json
import os
from engine import generate_excel_report


def get_previous_day_date_range():
    """Get the date range for the previous day.
    
    Returns:
        tuple: (from_date, to_date) as strings in format "YYYY-MM-DD HH:MM"
    """
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    from_date = yesterday.strftime('%Y-%m-%d 00:00')
    to_date = today.strftime('%Y-%m-%d 00:00')
    
    return from_date, to_date


def schedule_reports():
    """Schedule and run Excel report generation for configured reports."""
    # Get the previous day's date range
    from_date, to_date = get_previous_day_date_range()
    
    # Define reports to schedule
    reports_to_run = ['sample_v1', 'sample_v2']
    
    print(f"Running scheduled reports with date range: {from_date} to {to_date}")
    
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
                    'from_date': from_date,
                    'to_date': to_date
                }
            }
            
            # Add dataset parameters for each dataset in the report
            for dataset_id in dataset_ids:
                params[dataset_id] = {
                    'from_date': from_date,
                    'to_date': to_date
                }
                print(f"Added dataset parameter: {dataset_id} (from: {from_date}, to: {to_date})")
            
            print(f"Generating Excel report with {len(dataset_ids)} dataset(s)...")
            
            # Generate Excel report
            output_path = generate_excel_report(report_id, params)
            print(f"\n✓ Excel report generated successfully: {output_path}")
            
        except FileNotFoundError as e:
            print(f"\n✗ Error: Report or dataset not found for {report_id}: {e}")
        except Exception as e:
            print(f"\n✗ Error generating report {report_id}: {e}")


if __name__ == '__main__':
    schedule_reports()
