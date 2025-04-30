import yaml

def load_yaml_layout(file_path, command_mapping=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            layout = yaml.safe_load(f)
            # Map commands if a mapping is provided
            if command_mapping:
                for menu_name, items in layout.items():
                    for item in items:
                        if isinstance(item, dict) and "command" in item:
                            item["command"] = command_mapping.get(item["command"])
            return layout
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Fehler beim Laden der YAML-Datei: {e}")
        return {}