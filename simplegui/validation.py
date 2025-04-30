
import re

class Validator:
    @staticmethod
    def is_not_empty(value):
        return bool(value.strip())

    @staticmethod
    def matches_regex(value, pattern):
        return re.match(pattern, value) is not None

    @staticmethod
    def validate(fields, rules):
        errors = {}
        for field_name, validators in rules.items():
            value = fields.get(field_name, "")
            for validator_func, message in validators:
                if not validator_func(value):
                    errors[field_name] = message
                    break
        return errors
