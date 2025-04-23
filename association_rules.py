import pandas as pd

# Load association rules
rules_path = 'D:/Market Analysis Internhip Task/association_rules.csv'
rules = pd.read_csv(rules_path)

# Set thresholds for metrics
min_confidence = 0.7
min_lift = 1.2

# Filter strong rules
strong_rules = rules[(rules['confidence'] >= min_confidence) & (rules['lift'] >= min_lift)]

# Display strong rules
print("Strong Rules:")
print(strong_rules)

# Save strong rules
strong_rules_path = 'D:/Market Analysis Internhip Task/strong_rules.csv'
strong_rules.to_csv(strong_rules_path, index=False)
print(f"Strong rules saved to {strong_rules_path}.")
