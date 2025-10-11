import os

print("--- Path and File Diagnostic Script ---")

# 1. Print the Current Working Directory
try:
    cwd = os.getcwd()
    print(f"OK - Current Working Directory is: {cwd}")
except Exception as e:
    print(f"ERROR - Could not get Current Working Directory: {e}")

# 2. Check for the 'Models' folder and list its contents
try:
    models_path = os.path.join(cwd, 'Models')
    print(f"\nChecking for folder at: {models_path}")
    
    if os.path.isdir(models_path):
        print("OK - 'Models' folder FOUND.")
        files_in_models = os.listdir(models_path)
        print("\n--- Files found inside 'Models' ---")
        if files_in_models:
            for filename in files_in_models:
                print(f"  - {filename}")
        else:
            print("  - The 'Models' folder is empty.")
        print("---------------------------------")
    else:
        print("CRITICAL ERROR - 'Models' folder NOT FOUND at this location.")

except Exception as e:
    print(f"ERROR - An error occurred while checking the Models folder: {e}")

print("\n--- End of Report ---")