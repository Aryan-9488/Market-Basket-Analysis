import pandas as pd
from itertools import combinations

# Load frequent itemsets from CSV
frequent_itemsets = pd.read_csv("frequent_itemsets.csv")

# Ensure the 'itemsets' column contains frozenset objects
def convert_to_frozenset(itemset):
    if isinstance(itemset, str):
        return frozenset(eval(itemset))
    elif isinstance(itemset, tuple):
        return frozenset(itemset)
    return frozenset(itemset)

frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(convert_to_frozenset)

# Display the structure of frequent itemsets
print(frequent_itemsets.head())
print(frequent_itemsets.dtypes)

# Function to calculate association rules manually
def calculate_association_rules(frequent_itemsets, min_confidence=0.6):
    rules = []
    # Convert itemsets to dictionary for quick lookup
    support_dict = {tuple(itemset): support for itemset, support in zip(frequent_itemsets['itemsets'], frequent_itemsets['support'])}

    for itemset in frequent_itemsets['itemsets']:
        if len(itemset) < 2:
            continue  # Skip single-item sets as they can't generate rules

        for antecedent_size in range(1, len(itemset)):
            for antecedent in combinations(itemset, antecedent_size):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent

                # Skip invalid rules
                if len(consequent) == 0:
                    continue

                # Calculate confidence
                antecedent_support = support_dict.get(tuple(antecedent), 0)
                itemset_support = support_dict.get(tuple(itemset), 0)
                confidence = itemset_support / antecedent_support if antecedent_support > 0 else 0

                # Add rule if confidence meets the threshold
                if confidence >= min_confidence:
                    lift = confidence / support_dict.get(tuple(consequent), 1)
                    rules.append({
                        "antecedents": antecedent,
                        "consequents": consequent,
                        "support": itemset_support,
                        "confidence": confidence,
                        "lift": lift
                    })

    return pd.DataFrame(rules)

# Calculate association rules with confidence >= 0.6
rules = calculate_association_rules(frequent_itemsets, min_confidence=0.6)

# Display top 10 rules sorted by confidence
top_rules = rules.nlargest(10, 'confidence')
print("Top 10 Association Rules:")
print(top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Save the top 10 rules to a CSV file
top_rules.to_csv("top_association_rules.csv", index=False)
print("Top rules have been saved to 'top_association_rules.csv'.")
