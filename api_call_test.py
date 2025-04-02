import urllib.request, json
import pandas as pd
with urllib.request.urlopen("https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/PEA15/JSON-stat/2.0/en") as url:
    data = json.load(url)
print(data)


# Process JSON-stat format to pandas DataFrame
# This part depends on the structure of the response
# Example basic processing:
dimensions = data['dimension']
values = data['value']

# Create a DataFrame based on the specific structure
# This is a simplified example - you'll need to adapt it
# Creating the dataframe from the JSON structure
df = pd.DataFrame(data['value'], columns=['Value'])

# Mapping the years and components
df['Year'] = list(data['TLIST(A1)']['category']['index'])[:len(df)]  # Assign the years
df['Component'] = 'Net migration'  # Assuming we are interested in net migration for this case

# Filtering for the "Net migration" data
df_filtered = df[df['Component'] == 'Net migration']

# Displaying the result
print(df_filtered)
# Process based on the specific structure of the dataset
# More processing code would go here

