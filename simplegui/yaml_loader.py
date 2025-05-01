import yaml

def load_yaml_layout(file_path, command_mapping=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            layout = yaml.safe_load(f)
            # Map commands if a mapping is provided
            if command_mapping:
                for key, items in layout.items():
                    if key == "grid":  # Handle grid layout
                        for item in items:
                            if "options" in item and "command" in item["options"]:
                                item["options"]["command"] = command_mapping.get(item["options"]["command"])
                    elif key == "rows":  # Handle rows layout
                        for row in items:
                            for column in row.get("columns", []):
                                if "options" in column and "command" in column["options"]:
                                    column["options"]["command"] = command_mapping.get(column["options"]["command"])
            return layout
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Fehler beim Laden der YAML-Datei: {e}")
        return {}