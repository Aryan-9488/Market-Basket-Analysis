import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def load_basket_data(file_path):
    """Load the basket matrix from the preprocessed CSV file."""
    print("Loading basket data...")
    basket_data = pd.read_csv(file_path)
    # Convert to boolean type for performance optimization
    basket_data = basket_data.astype(bool)
    print("Basket data loaded successfully.")
    return basket_data

def apply_apriori(basket_data, min_support):
    """Apply the Apriori algorithm to find frequent itemsets."""
    print("Applying Apriori algorithm...")
    frequent_itemsets = apriori(basket_data, min_support=min_support, use_colnames=True)
    print(f"Found {len(frequent_itemsets)} frequent itemsets.")
    return frequent_itemsets

def generate_association_rules(frequent_itemsets, metric, min_threshold):
    """Generate association rules from the frequent itemsets."""
    print("Generating association rules...")
    # Count the number of frequent itemsets
    num_itemsets = len(frequent_itemsets)
    # Pass the num_itemsets argument
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold, num_itemsets=num_itemsets)
    print(f"Generated {len(rules)} association rules.")
    return rules


def save_results(frequent_itemsets, rules, output_path_itemsets, output_path_rules):
    """Save the frequent itemsets and association rules to CSV files."""
    frequent_itemsets.to_csv(output_path_itemsets, index=False)
    print(f"Frequent itemsets saved to {output_path_itemsets}.")
    
    rules.to_csv(output_path_rules, index=False)
    print(f"Association rules saved to {output_path_rules}.")

if __name__ == "__main__":
    # File paths
    basket_data_file = 'D:/Market Analysis Internhip Task/basket_data.csv'
    output_itemsets_file = 'D:/Market Analysis Internhip Task/frequent_itemsets.csv'
    output_rules_file = 'D:/Market Analysis Internhip Task/association_rules.csv'

    # Load the preprocessed basket matrix
    basket_data = load_basket_data(basket_data_file)

    # Step 1: Apply Apriori Algorithm
    min_support = 0.01  # Adjust the minimum support as needed
    frequent_itemsets = apply_apriori(basket_data, min_support)

    # Step 2: Generate Association Rules
    metric = "lift"  # Metric to evaluate association rules
    min_threshold = 1.0  # Minimum threshold for the chosen metric
    rules = generate_association_rules(frequent_itemsets, metric, min_threshold)

    # Step 3: Save Results
    save_results(frequent_itemsets, rules, output_itemsets_file, output_rules_file)

    print("Apriori algorithm completed successfully.")
