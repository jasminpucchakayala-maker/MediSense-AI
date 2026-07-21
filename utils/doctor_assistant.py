def generate_advice(disease):

    advice = {

        "Common Cold": {
            "causes": [
                "Viral infection",
                "Exposure to cold weather",
                "Low immunity"
            ],

            "actions": [
                "Drink enough fluids",
                "Take adequate rest",
                "Maintain hygiene"
            ],

            "doctor": 
                "Consult a doctor if symptoms persist or worsen.",

            "prevention": [
                "Wash hands regularly",
                "Avoid close contact with infected people"
            ]
        }

    }


    return advice.get(
        disease,
        {
            "causes": [
                "Multiple factors may contribute to this condition."
            ],

            "actions": [
                "Maintain a healthy lifestyle",
                "Monitor symptoms carefully"
            ],

            "doctor":
                "Consult a healthcare professional for proper evaluation.",

            "prevention": [
                "Follow healthy habits",
                "Regular health checkups"
            ]
        }
    )