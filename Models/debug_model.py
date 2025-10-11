import pickle

model_path = "Models/linear_asset_models.pkl"
features_path = "Models/linear_feature_columns.pkl"

with open(model_path, "rb") as f:
    obj = pickle.load(f)

print("\n=== MODEL CONTENTS ===")
print("Type:", type(obj))

if isinstance(obj, dict):
    print("Keys:", list(obj.keys()))
    for k, v in obj.items():
        print(f" - {k}: {type(v)}")

with open(features_path, "rb") as f:
    features = pickle.load(f)

print("\n=== FEATURE COLUMNS ===")
if isinstance(features, dict):
    print("Dict keys:", list(features.keys())[:10], "...")
else:
    print("List of features:", features[:10], "...")
print("Total features:", len(features))
