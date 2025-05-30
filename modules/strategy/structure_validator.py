import yaml
from jsonschema import validate, exceptions as jsonschema_exceptions
import pprint

def verify(structure):
    pprint.pprint(structure)
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "oneOf": [
                {
                    "properties": {
                        "move": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["named", "absolute", "relative"]},
                                "target": {"type": "string"},
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "w": {"type": "number"}
                            },
                            "required": ["type"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["move"],
                    "additionalProperties": False
                },
                {
                    "properties": {
                        "effect": {
                            "type": "object",
                            "properties": {
                                "take": {"type": "array", "items": {"type": "integer"}},
                                "release": {"type": "array", "items": {"type": "integer"}}
                            },
                            "additionalProperties": False
                        }
                    },
                    "required": ["effect"],
                    "additionalProperties": False
                },
                {
                    "properties": {
                        "wait": {"type": "number"}
                    },
                    "required": ["wait"],
                    "additionalProperties": False
                }
            ]
        }
    }

    try:
        validate(instance=structure, schema=schema)
        print("✅ Stratégie YAML valide !")
    except jsonschema_exceptions.ValidationError as e:
        print("❌ Erreur de validation :", e.message)

with open("configuration/strategy.yml") as f:
    data = yaml.safe_load(f)
    print("Type YAML chargé :", type(data))
    verify(data)
