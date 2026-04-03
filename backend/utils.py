def preprocess_input(form_data):
    age = int(form_data["age"])
    sex = int(form_data["sex"])
    cp = int(form_data["cp"])
    trestbps = float(form_data["trestbps"])
    chol = float(form_data["chol"])
    fbs = int(form_data["fbs"])
    restecg = int(form_data["restecg"])
    thalach = float(form_data["thalach"])
    exang = int(form_data["exang"])
    oldpeak = float(form_data["oldpeak"])

    # Keep encoded values exactly as submitted by form. These must match
    # the feature encoding used in model training.
    slope = int(form_data["slope"])
    thal = int(form_data["thal"])

    ca = int(form_data["ca"])

    return [age, sex, cp, trestbps, chol, fbs,
            restecg, thalach, exang, oldpeak,
            slope, ca, thal]