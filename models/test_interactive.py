# Allow the user to submit test inputs directly and get model predictions
import joblib

# Load the trained model and vectorizer
model = joblib.load('v1/lr_model_v1.joblib')
vectorizer = joblib.load('v1/vectorizer_v1.joblib')

def predict_email(sender="", receiver="", subject="", body="", urls="") -> int:
    # Preprocess the input
    input_text = f"{sender.lower()} {receiver.lower()} {subject.lower()} {body.lower()} {urls.lower()}"
    
    # Transform the input using the loaded vectorizer
    input_tfidf = vectorizer.transform([input_text])
    
    # Make prediction using the loaded model
    prediction = model.predict(input_tfidf)

    return 1 if prediction[0] == 1 else 0 # Return 1 for phishing, 0 for legit

