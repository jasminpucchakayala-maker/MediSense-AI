def calculate_risk(confidence, symptom_count):

    if confidence >= 85 and symptom_count >= 5:
        return {
            "level": "High",
            "color": "🔴",
            "message": "Multiple symptoms detected with high prediction confidence. Consider consulting a healthcare professional."
        }

    elif confidence >= 60:
        return {
            "level": "Medium",
            "color": "🟠",
            "message": "Symptoms indicate a possible condition. Monitor symptoms and seek medical advice if needed."
        }

    else:
        return {
            "level": "Low",
            "color": "🟢",
            "message": "Prediction confidence is lower. Additional medical evaluation may be helpful."
        }