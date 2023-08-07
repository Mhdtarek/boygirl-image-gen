import json
import random

def scramble_json_arrays(data):
    if isinstance(data, list):
        random.shuffle(data)
        for item in data:
            if isinstance(item, list) or isinstance(item, dict):
                scramble_json_arrays(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, dict):
                scramble_json_arrays(value)

if __name__ == "__main__":
    file_path = input("Enter the path of the JSON file to scramble: ")

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        scramble_json_arrays(json_data)

        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)

        print("JSON file has been scrambled successfully.")
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
