import json

def save_configs(user_configs):
    with open('user_configs.json', 'w') as f:
        json.dump(user_configs, f, indent=4)

def load_configs():
    try:
        with open('user_configs.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

if __name__ == '__main__':
    save_configs()
    load_configs()
        