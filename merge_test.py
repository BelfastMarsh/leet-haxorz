import pandas as pd
import requests
import json

def get_cso_data(table_id, variables=None):
    """
    Fetch data from CSO PxStat API
    
    Args:
        table_id: The ID of the table to fetch
        variables: Dictionary of variables to filter by
    
    Returns:
        pandas DataFrame with the results
    """
    url = f"https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/{table_id}/JSON-stat/2.0/en"
    print(url)
    # If variables are specified, add them to the request
    if variables:
        params = {
            "query": json.dumps({"request": variables}),
            "format": "json-stat2"
        }
        response = requests.get(url, params=params)
    else:
        response = requests.get(url)
        print(response)
    
    if response.status_code == 200:
        data = response.json()
        
        # Process JSON-stat format to pandas DataFrame
        # This part depends on the structure of the response
        # Example basic processing:
        dimensions = data['dimension']
        values = data['value']
        
        # Create a DataFrame based on the specific structure
        # This is a simplified example - you'll need to adapt it
        results = json.load(data)
        # Process based on the specific structure of the dataset
        # More processing code would go here
        
        return pd.DataFrame(results)
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

# Function to get migration data
def get_migration_data():
    """
    Get migration data from CSO
    
    Table code for migration: PEA15 (Population and Migration Estimates)
    """
    # In reality, you would do:
    years = list(range(2010, 2024))
    df = get_cso_data("PEA15")
#    data = {"Year" : years, "Net_Migration_Thousands" : df.Immigration - df.Emigration}
    # Then calculate net migration as Immigration - Emigration

    return pd.DataFrame(df)

print(get_migration_data())
