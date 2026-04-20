knowledge_base = [
    {
        "topic": "raw_biometric_data",
        "rule": "Raw biometric data must not be used for AI model training by default.",
        "conditions": [
            "Explicit user consent is obtained",
            "Data is anonymized",
            "Usage is clearly disclosed"
        ],
        "examples": [
            "Using heart rate data without consent → NOT allowed",
            "Using anonymized heart rate data with consent → allowed"
        ],
        "applicable_roles": ["data_scientist", "engineer"],
        "role_guidance": {
            "data_scientist": "Avoid using raw biometric data unless anonymization and consent are verified.",
            "engineer": "Ensure pipelines enforce anonymization before training."
        }
    },
    {
        "topic": "data_retention",
        "rule": "User health data should not be stored indefinitely.",
        "conditions": [
            "Retention period is defined",
            "User consent is obtained",
            "Data deletion mechanisms exist"
        ],
        "examples": [
            "Storing sleep data forever → NOT allowed",
            "Storing data for 30 days with consent → allowed"
        ],
        "applicable_roles": ["product_manager", "engineer"],
        "role_guidance": {
            "product_manager": "Define clear retention policies.",
            "engineer": "Implement automated deletion."
        }
    }
]
