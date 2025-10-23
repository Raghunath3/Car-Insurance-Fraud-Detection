# Car-Insurance-Fraud-Detection
A machine learning web app that predicts car insurance claim fraud using Django and a trained ML model. The system collects user details, processes them via a .pkl model, and displays fraud probability. Includes policy validation, database logging, and an admin dashboard for claim analysis.

🧾 Car Insurance Fraud Detection System

This project is a Django-based web application that predicts whether a car insurance claim is fraudulent or legitimate using a trained machine learning model.
It also includes a policy verification feature that ensures customers are eligible before submitting a claim.

🚀 Key Features

Policy Number Validation: Users must first enter their policy number, which is verified against backend customer data.

Eligibility Check: Automatically checks policy conditions like policy limits, expiry date, and premium criteria before allowing predictions.

Fraud Prediction Model: Uses a trained Random Forest model (rf_model.pkl) to detect fraudulent claims.

Business Rules: Adds domain-specific fraud detection overrides for low credit scores, drunk driving, or repeated accidents.

Automatic Payout Calculation: Calculates eligible claim payout based on premium, severity, and driving history.

Database Integration: Saves all prediction results and contact queries in the Django database.

User Interface: Simple and responsive HTML frontend connected to Django views and APIs.

🧠 Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

Machine Learning: Scikit-learn, Pandas, Joblib

Database: SQLite3 (default Django DB)

Model Files: rf_model.pkl, scaler.pkl, imputer.pkl, gender_encoder.pkl

📊 Workflow

User enters a policy number.

System checks eligibility based on policy details (expiry date, premium, and policy limits).

If valid, the prediction form appears with prefilled customer details.

Model predicts claim as Fraudulent or Legitimate.

Payout is calculated and logged in the backend.

⚙️ Future Enhancements

Integrate live policy API verification.

Add admin dashboard for tracking fraud trends.

Enable automated email alerts for flagged claims.
