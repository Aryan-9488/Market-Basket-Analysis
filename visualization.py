import pandas as pd
import matplotlib.pyplot as plt

# Load frequent itemsets and item descriptions
frequent_itemsets = pd.read_csv("frequent_itemsets.csv")
online_retail = pd.read_csv("online_retail.csv")

# Ensure descriptions are strings and handle NaN values
online_retail['Description'] = online_retail['Description'].fillna("Unknown").astype(str)

# Create a mapping from StockCode to Description
description_mapping = online_retail[['StockCode', 'Description']].drop_duplicates()
description_mapping = description_mapping.set_index('StockCode')['Description'].to_dict()

# Function to map StockCodes to their descriptions
def map_to_descriptions(itemset):
    descriptions = [description_mapping.get(stock_code, f"Unknown ({stock_code})") for stock_code in eval(itemset)]
    return ', '.join(descriptions)

# Map itemsets to their descriptions
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(map_to_descriptions)

# Sort frequent itemsets by support and take the top 10
top_10 = frequent_itemsets.nlargest(10, 'support')

# Plot the top 10 frequent itemsets with descriptions
plt.figure(figsize=(10, 6))
plt.barh(top_10['itemsets'], top_10['support'], color='skyblue')
plt.xlabel('Support')
plt.ylabel('Itemsets')
plt.title('Top 10 Frequent Itemsets (with Descriptions)')
plt.gca().invert_yaxis()
plt.tight_layout()

# Show the plot
plt.show()
