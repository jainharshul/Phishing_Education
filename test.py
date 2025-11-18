from phishing_model import predict_email

email_text = "Verify your password now or your account will be closed!"

result_svm = predict_email(email_text, model="svm")
result_logreg = predict_email(email_text, model="logreg")  # optional

print("SVM:", result_svm)
print("LogReg:", result_logreg)
