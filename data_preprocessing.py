import pandas as pd

# Load the dataset
def load_data(file_path):
    """Loads the dataset from a CSV file."""
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    return df

# Clean the dataset
def clean_data(df):
    """Cleans the dataset by dropping unnecessary columns, handling missing values, 
    and ensuring positive values for Quantity and UnitPrice."""
    # Drop irrelevant columns
    df.drop(columns=['InvoiceDate', 'Country'], inplace=True)

    # Handle missing values
    df.dropna(subset=['StockCode', 'Quantity', 'UnitPrice', 'CustomerID'], inplace=True)

    # Filter for positive Quantity and UnitPrice
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    
    # Reset index to avoid issues
    df.reset_index(drop=True, inplace=True)

    return df

# Create a list of items per transaction
def create_item_list(df):
    """Groups transactions by InvoiceNo and creates a list of items for each transaction."""
    basket = df.groupby('InvoiceNo')['StockCode'].apply(lambda x: list(set(x))).reset_index(name='Items')
    del df  # Free memory after processing
    return basket

# Create the basket matrix in a one-hot encoded format
def create_basket_matrix(basket):
    """Converts the list of items into a one-hot encoded basket matrix."""
    # Explode all items into a unique list
    all_items = basket['Items'].explode().unique()

    # Create a one-hot encoded matrix
    basket_matrix = basket['Items'].apply(lambda x: pd.Series(1, index=x)).fillna(0)
    
    # Ensure all transactions have the same column set
    basket_matrix = basket_matrix.reindex(columns=all_items, fill_value=0)
    
    del basket  # Free memory after processing
    return basket_matrix

# Main preprocessing function
def preprocess_data(file_path):
    """Main preprocessing function to clean data, create basket matrix, and save the result."""
    print("Starting preprocessing...")

    # Step 1: Load data
    df = load_data(file_path)
    print("Data loaded successfully.")

    # Step 2: Clean data
    cleaned_data = clean_data(df)
    print("Data cleaned successfully.")
    del df  # Free memory after cleaning data

    # Step 3: Create item lists
    basket = create_item_list(cleaned_data)
    print("Item lists created successfully.")
    del cleaned_data  # Free memory after creating item lists

    # Step 4: Create basket matrix
    basket_matrix = create_basket_matrix(basket)
    print("Basket matrix created successfully.")

    # Step 5: Save to CSV
    basket_matrix.to_csv('D:/Market Analysis Internhip Task/basket_data.csv', index=False)
    print("Basket matrix saved to basket_data.csv.")
    del basket_matrix  # Free memory after saving the basket matrix

if __name__ == "__main__":
    file_path = 'D:/Market Analysis Internhip Task/online_retail.csv'  # Update as per your file path
    preprocess_data(file_path)
