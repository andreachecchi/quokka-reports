import requests
import csv
import io
import re


def fetch_data(dataset_config, dataset_dir):
    """
    Graylog implementation of data fetching.
    
    Args:
        dataset_config: Full dataset configuration dictionary
        dataset_dir: Directory containing the dataset
    
    Returns:
        Dictionary with 'columns' and 'rows' keys
    """
    db = dataset_config['database']
    
    # Get query - use explicit query from config
    query = dataset_config.get('query', '*')
    
    # Get the parameters passed from generate_report
    param_values = dataset_config.get('_params', {})
    
    # Build time range
    time_range = dataset_config.get('time_range', {})
    from_time = param_values.get('from', time_range.get('from', '2025-01-01T00:00:00.000Z'))
    to_time = param_values.get('to', time_range.get('to', '2027-01-02T00:00:00.000Z'))
    
    # Ensure timestamps are in correct format: YYYY-MM-DDTHH:MM:SS.000Z
    def normalize_timestamp(timestamp):
        """Complete timestamp with missing seconds and milliseconds if needed"""
        # Pattern for YYYY-MM-DDTHH:MM format (missing seconds)
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$', timestamp):
            return timestamp + ':00.000Z'
        # Pattern for YYYY-MM-DDTHH:MM:SS format (missing milliseconds)
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$', timestamp):
            return timestamp + '.000Z'
        return timestamp
    
    from_time = normalize_timestamp(from_time)
    to_time = normalize_timestamp(to_time)
    
    # Get fields from config or use default
    fields = dataset_config.get('fields', ['timestamp', 'source', 'message', 'gdpr'])
    fields_str = ','.join(fields)
    
    # Build URL and parameters
    url = f"{db['url']}/api/search/universal/absolute/export"
    
    # Prepare auth - Graylog uses token as username with 'token' as password
    # Or username/password for basic auth
    if 'token' in db:
        auth = (db['token'], 'token')
    else:
        auth = (db['username'], db['password'])
    
    # Prepare request parameters
    params = {
        'query': query,
        'from': from_time,
        'to': to_time,
        'fields': fields_str
    }
    
    # Prepare headers
    headers = {
        'Accept': 'text/csv'
    }
    
    # Make request
    response = requests.get(
        url,
        params=params,
        headers=headers,
        auth=auth
    )
    
    response.raise_for_status()
    
    # Parse CSV response
    csv_content = response.text
    
    if not csv_content.strip():
        return {'columns': fields, 'rows': []}
    
    # Parse CSV
    reader = csv.reader(io.StringIO(csv_content))
    rows = list(reader)
    
    # First row is usually headers
    columns = rows[0] if rows else fields
    data_rows = rows[1:] if len(rows) > 1 else []
    
    return {
        'columns': columns,
        'rows': data_rows
    }
