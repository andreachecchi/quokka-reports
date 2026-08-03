import psycopg2


def fetch_data(dataset_config):
    """
    PostgreSQL implementation of data fetching.
    
    Args:
        dataset_config: Full dataset configuration dictionary
    
    Returns:
        Dictionary with 'columns' and 'rows' keys
    """
    db = dataset_config['database']
    query = dataset_config['query']
    
    # If query starts with '@', read from file
    if query.startswith('@'):
        filename = query[1:]  # Remove the '@' prefix
        # Get the directory of the current file to construct full path
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        query_file_path = os.path.join(current_dir, filename)
        with open(query_file_path, 'r') as f:
            query = f.read()
    
    params = dataset_config.get('params', [])
    
    # Get the parameters passed from generate_report
    param_values = dataset_config.get('_params', {})
    
    # Substitute ${param_name} with actual values
    for param in params:
        param_id = param['id']
        if param_id in param_values:
            value = param_values[param_id]
            # Escape value for SQL (simple approach - in production use proper parametrization)
            if param.get('type') == 'datetime':
                query = query.replace(f'${{{param_id}}}', f"'{value}'")
            else:
                query = query.replace(f'${{{param_id}}}', f"'{value}'" if isinstance(value, str) else str(value))
    
    # Connect to database
    conn = psycopg2.connect(
        host=db['host'],
        port=db['port'],
        database=db['name'],
        user=db['username'],
        password=db['password']
    )
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        return {
            'columns': columns,
            'rows': rows
        }
    finally:
        cursor.close()
        conn.close()
