from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    name = request.form["name"]
    age = int(request.form["age"])
    gender = request.form["gender"]
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    bp = int(request.form["bp"])
    condition = request.form["condition"]
    treatment = request.form["treatment"]

    symptoms = request.form.getlist("symptoms")
    other_symptom = request.form["other_symptom"]

    # BMI
    bmi = round(weight / ((height / 100) ** 2), 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # BP
    if bp < 120:
        bp_status = "Normal"
    elif bp < 140:
        bp_status = "Pre-High"
    else:
        bp_status = "High"

    # Risk Score
    risk_score = 0

    if bmi_status in ["Overweight", "Obese"]:
        risk_score += 1
    if bp_status == "High":
        risk_score += 2
    elif bp_status == "Pre-High":
        risk_score += 1
    if condition != "None":
        risk_score += 2
    if treatment == "Yes":
        risk_score += 1

    if "Chest Pain" in symptoms:
        risk_score += 2
    if "Breathing Difficulty" in symptoms:
        risk_score += 2
    if "High Sugar" in symptoms:
        risk_score += 1

    if risk_score >= 6:
        risk_level = "High Risk"
    elif risk_score >= 3:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    # Summary & Advice
    if "Chest Pain" in symptoms:
        summary = "Possible heart-related condition detected."
        advice = [
            "Consult cardiologist immediately",
            "Avoid heavy physical activity",
            "Monitor blood pressure daily"
        ]
    elif "Fever" in symptoms or "Cough" in symptoms:
        summary = "Possible infection detected."
        advice = [
            "Take proper rest",
            "Drink warm fluids",
            "Consult doctor if symptoms continue"
        ]
    elif "Diarrhea" in symptoms or "Vomiting" in symptoms:
        summary = "Digestive issue suspected."
        advice = [
            "Drink ORS",
            "Eat light food",
            "Avoid oily food"
        ]
    elif condition != "None":
        summary = f"Existing condition: {condition}. Regular monitoring required."
        advice = [
            "Follow prescribed medication",
            "Routine specialist check-up"
        ]
    else:
        summary = "No serious symptoms detected."
        advice = [
            "Maintain healthy diet",
            "Regular exercise",
            "Annual health checkup"
        ]

    return render_template("result.html",
                           name=name,
                           age=age,
                           gender=gender,
                           bmi=bmi,
                           bmi_status=bmi_status,
                           bp=bp,
                           bp_status=bp_status,
                           condition=condition,
                           treatment=treatment,
                           symptoms=symptoms,
                           other_symptom=other_symptom,
                           risk_level=risk_level,
                           summary=summary,
                           advice=advice)

if __name__ == "__main__":
    app.run(debug=True)