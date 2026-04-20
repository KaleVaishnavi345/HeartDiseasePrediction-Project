import json
import os
from flask import render_template, request, redirect, url_for, flash, session
from app import app
from backend.predict import predict_heart
from backend.utils import preprocess_input

# ---------------- DATABASE ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "..", "users.json")

def load_users():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# ---------------- LOGIN ----------------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email]['password'] == password:
            session['user_name'] = users[email]['username']
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password")

    return render_template('login.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        email = request.form.get('email')

        if email in users:
            flash("Email already exists")
            return redirect(url_for('register'))

        users[email] = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'phone': request.form.get('phone')
        }

        save_users(users)
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_name' in session:
        return render_template('dashboard.html', username=session['user_name'])
    return redirect(url_for('login'))


# ---------------- PREDICTION FORM ----------------
@app.route('/prediction_form')
def prediction_form():
    if 'user_name' in session:
        return render_template('prediction_form.html')
    return redirect(url_for('login'))

@app.route('/normal_ranges')
def normal_ranges():
    if 'user_name' in session:
        return render_template('normal_ranges.html')
    return redirect(url_for('login'))


# ---------------- PREDICTION ----------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'user_name' not in session:
        return redirect(url_for('login'))

    try:
        form_data = request.form
        selected_model = form_data.get("model_name", "ensemble")

        # Step 1: preprocess form input
        processed_data = preprocess_input(form_data)

        print("Processed Data:", processed_data)

        # Step 2: get ML-based class and confidence
        prediction_output = predict_heart(processed_data, selected_model)
        confidence = prediction_output["confidence"]
        prediction_class = prediction_output["prediction_class"]
        model_used = prediction_output["model_used"]
        high_risk_probability = prediction_output["high_risk_probability"]
        low_risk_probability = prediction_output["low_risk_probability"]

        # Step 3: risk comes directly from model class output
        if prediction_class == 0:
            result = "High Risk of Heart Disease"
        else:
            result = "Low Risk of Heart Disease"

        return render_template(
            'result.html',
            prediction=result,
            probability=confidence,
            high_risk_probability=high_risk_probability,
            low_risk_probability=low_risk_probability,
            model_used=model_used
        )

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))