from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import pandas as pd
import json
import joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from .models import Prediction, Contact


# Load the model once
model = joblib.load('fraudapp/ml/rf_model.pkl')

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')


# Business Rule Override
def enhanced_fraud_detection(input_df, model_prob):
    if (input_df['Credit Score'].iloc[0] < 500 or
        input_df['Drunk Driving History'].iloc[0] == 1 or
        (input_df['Past Accidents'].iloc[0] > 2 and input_df['Accident Severity'].iloc[0] == 3) or
        (input_df['Driving Experience'].iloc[0] < 3 and input_df['Past Accidents'].iloc[0] > 1)):
        return 1.0
    return model_prob

# Dynamic threshold logic
def calculate_threshold(input_df):
    base = 0.45
    risk = 0
    if input_df['Credit Score'].iloc[0] < 600: risk += 0.15
    if input_df['Drunk Driving History'].iloc[0] == 1: risk += 0.25
    if input_df['Past Accidents'].iloc[0] > 1: risk += 0.1 * input_df['Past Accidents'].iloc[0]
    if input_df['Accident Severity'].iloc[0] == 3: risk += 0.2
    return min(base + risk, 0.9)

# Payout logic
def calculate_payout(input_df, is_legitimate):
    if not is_legitimate:
        return 0.0

    multipliers = {1: 0.2, 2: 0.3, 3: 0.4}
    severity = input_df['Accident Severity'].iloc[0]
    premium = input_df['Premium Amount'].iloc[0]
    base = premium * multipliers.get(severity, 0.2)

    discount = 0
    if input_df['Credit Score'].iloc[0] > 700: discount += 0.05
    if input_df['Speeding History'].iloc[0] == 0: discount += 0.05
    if input_df['Drunk Driving History'].iloc[0] == 0: discount += 0.10

    payout = base * (1 + discount)
    return min(payout, premium * 0.5)

@csrf_exempt
def predict_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Convert string inputs like 'Yes'/'No' and normalize gender
            drunk = 1 if str(data.get('drunk', '')).strip().lower() == 'yes' else 0
            gender = 1 if str(data.get('gender', '')).strip().lower() == 'male' else 0

            input_data = {
                'Credit Score': [float(data['credit_score'])],
                'Policy Holder Age': [int(data['age'])],
                'Driving Experience': [int(data['experience'])],
                'Speeding History': [int(data['speeding'])],
                'Past Accidents': [int(data['accidents'])],
                'Accident Severity': [int(data['severity'])],
                'Gender': [gender],
                'Drunk Driving History': [drunk],
                'Premium Amount': [float(data['premium'])],
            }

            input_df = pd.DataFrame(input_data)

            # Impute and scale
            imputer = SimpleImputer(strategy='mean')
            input_imputed = pd.DataFrame(imputer.fit_transform(input_df), columns=input_df.columns)

            scaler = StandardScaler()
            input_scaled = pd.DataFrame(scaler.fit_transform(input_imputed), columns=input_df.columns)

            # Predict
            try:
                base_prob = model.predict_proba(input_scaled[model.feature_names_in_])[0][1]
            except AttributeError:
                base_prob = model.predict_proba(input_scaled)[0][1]

            fraud_prob = enhanced_fraud_detection(input_df, base_prob)
            threshold = calculate_threshold(input_df)
            is_fraud = fraud_prob > threshold
            payout = calculate_payout(input_df, not is_fraud)

            # Save to DB
            Prediction.objects.create(
                credit_score=input_data['Credit Score'][0],
                age=input_data['Policy Holder Age'][0],
                experience=input_data['Driving Experience'][0],
                speeding=input_data['Speeding History'][0],
                accidents=input_data['Past Accidents'][0],
                severity=input_data['Accident Severity'][0],
                gender=gender,
                drunk=drunk,
                premium=input_data['Premium Amount'][0],
                fraud_probability=fraud_prob,
                threshold=threshold,
                prediction='Fraudulent' if is_fraud else 'Legitimate',
                payout=round(payout, 2)
            )

            return JsonResponse({
                'prediction': 'Fraudulent' if is_fraud else 'Legitimate',
                'fraud_probability': round(fraud_prob, 2),
                'threshold': round(threshold, 2),
                'eligible_payout': round(payout, 2)
            })

        except Exception as e:
            print("❌ Prediction error:", str(e))
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def submit_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get("name")
            email = data.get("email")
            subject = data.get("subject", "")
            message = data.get("message")

            if not (name and email and message):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

