import re
import logging

class Validator:
    @staticmethod
    def is_not_empty(value):
        """
        Check if the given value is not empty or only whitespace.
        Returns True if value contains non-whitespace characters.
        """
        return bool(value.strip())

    @staticmethod
    def matches_regex(value, pattern):
        """
        Check if the given value matches the provided regular expression pattern.
        Returns True if the pattern matches, False otherwise.
        """
        return re.match(pattern, value) is not None

    @staticmethod
    def validate(fields, rules):
        """
        Validate a dictionary of fields against a set of validation rules.

        Args:
            fields (dict): Dictionary of field names to values.
            rules (dict): Dictionary of field names to a list of (validator_func, error_message) tuples.

        Returns:
            dict: A dictionary of field names to error messages for fields that failed validation.
        """
        errors = {}
        for field_name, validators in rules.items():
            value = fields.get(field_name, "")
            for validator_func, message in validators:
                if not validator_func(value):
                    errors[field_name] = message
                    break  # Stop at the first failed validator for this field
        return errors

    @staticmethod
    def validate_layout(layout, command_mapping, widget_class_mapping):
        """
        Validate that all referenced commands and widget types exist in the layout.
        Logs warnings for missing commands or widget types.

        Args:
            layout (dict): The loaded layout dictionary.
            command_mapping (dict): Mapping from command names to Python functions.
            widget_class_mapping (dict): Mapping from widget type names to widget classes.
        """
        def _recursive_validate(data):
            if isinstance(data, dict):
                # Check for command validity
                if "command" in data and isinstance(data["command"], str):
                    cmd = data["command"]
                    if cmd not in command_mapping:
                        logging.warning(f"Command '{cmd}' is referenced in layout but not found in command_mapping.")
                # Check for widget type validity
                if "type" in data:
                    widget_type = data["type"]
                    if widget_type not in widget_class_mapping:
                        logging.warning(f"Widget type '{widget_type}' is referenced in layout but not found in widget_class_mapping.")
                # Recurse into nested structures
                for value in data.values():
                    if isinstance(value, (dict, list)):
                        _recursive_validate(value)
            elif isinstance(data, list):
                for item in data:
                    _recursive_validate(item)
        _recursive_validate(layout)
