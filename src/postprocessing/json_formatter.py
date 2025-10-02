import os
import json

def save_json(data, folder_path, filename):
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
if __name__ == "__main__":
    sample_data = {"name": "Rahul", "task": "Test JSON save"}
    save_json(sample_data, folder_path="../data/interim", filename="test_output.json")
    print("✅ JSON saved successfully!")
