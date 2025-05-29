import jsonschema
from jsonschema import validate

def verify(structure):
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
                                "take": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                },
                                "release": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                }
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
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("❌ Erreur de validation :", e.message)
        return False
