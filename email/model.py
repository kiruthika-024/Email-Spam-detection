import joblib

model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')


spam_keywords = [
    "win", "won", "winner", "prize", "cash", "free", "offer", "bonus",
    "money", "click", "claim", "urgent", "congratulations", "gift",
    "credit", "loan", "discount", "deal", "limited", "act now"
]

print("📧 Email Spam Detector")
print("Type your message below. Type 'exit' to quit.\n")

while True:
    user_input = input("Your message: ")

    if user_input.lower() == 'exit':
        print("👋 Goodbye!")
        break

    if user_input.strip() == "":
        print("⚠️ Please enter a non-empty message.\n")
        continue

    input_vec = vectorizer.transform([user_input])
    prediction = model.predict(input_vec)[0]
    result = "🚫 Spam" if prediction == 1 else "✅ Not Spam"
    print(f"Result: {result}")

    if prediction == 1:
        words = user_input.lower().split()
        found_keywords = [word for word in words if word in spam_keywords]

        if found_keywords:
            print("🔑 Spam Keywords Found:", ", ".join(found_keywords))
        else:
            print("⚠️ Spam detected, but no known keywords matched.")

    print()
