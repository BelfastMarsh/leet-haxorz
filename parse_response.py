def parse_reponse(dimensions, values):
    dimension_compiled = {}
    for d in dimensions.keys():
        # dimension_compiled.append([])
        # print(dimensions[d]['category']['label'])
        tmparray = []
        for lst in dimensions[d]['category']['label'].keys():
            tmparray.append(dimensions[d]['category']['label'][lst])
        dimension_compiled[d] = tmparray

    n = 0
    lst2 = [[""]]
    while n < len(dimension_compiled):
        lst2.append([])
        for d in dimension_compiled[list(dimension_compiled.keys())[n]]:
            for l in lst2[n]:
                lst2[n + 1].append(l + "_" + d)
        n = n + 1

    m = 0
    data_dict = []
    for l in lst2[len(lst2) - 1]:
        tmpd = {}
        f = l.split("_")
        r = 1
        for lbl in list(dimension_compiled.keys()):
            tmpd[lbl] = f[r]
            r = r + 1
        tmpd["value"] = values[m]
        data_dict.append(tmpd)
        m = m + 1
    return data_dict



# Function to fetch data from CSO API
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
    
    # If variables are specified, add them to the request
    if variables:
        params = {
            "query": json.dumps({"request": variables}),
            "format": "json-stat2"
        }
        response = requests.get(url, params=params)
    else:
        response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Process JSON-stat format to pandas DataFrame
        # This part depends on the structure of the response
        # Example basic processing:
        dimensions = data['dimension']
        values = data['value']
        
        # Create a DataFrame based on the specific structure
        # This is a simplified example - you'll need to adapt it
        results = parse_reponse(dimensions, values)

        
        # Process based on the specific structure of the dataset
        # More processing code would go here
        
        return pd.DataFrame(results)
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

# Function to get potato yield data
import pandas as pd

def get_potato_data():
    """
    Get potato yield data from CSO
    For this example, I'm using a sample - replace with actual API call
    
    Table code for crops: AQA04 (Crop Yield and Production)
    """
    # In reality, you would do:
    data = get_cso_data("AQA04")
    
    return data
