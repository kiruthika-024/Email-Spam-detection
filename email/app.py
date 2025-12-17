import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


emails = [
    "Congratulations! You won a lottery, claim now",
    "Limited offer!!! Buy now",
    "Your Amazon order has been shipped",
    "Hi friend, let's meet tomorrow",
    "Earn money fast by clicking this link",
    "Reminder: project meeting at 3PM"
]
labels = [1, 1, 0, 0, 1, 0]  

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)

model = MultinomialNB()
model.fit(X, labels)
def check_spam(email):
    email_vector = vectorizer.transform([email])
    prediction = model.predict(email_vector)[0]
    return prediction


conn = sqlite3.connect('spam_detection.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS email_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_text TEXT,
    prediction TEXT
)
''')

def save_to_db(email, prediction):
    cursor.execute(
        "INSERT INTO email_results(email_text, prediction) VALUES (?, ?)",
        (email, prediction)
    )
    conn.commit()
    print("✅ Stored in database")


user_email = input("Enter email to check: ")

result = check_spam(user_email)
label = "Spam" if result == 1 else "Not Spam"

print(f"Prediction: {label}")

save_to_db(user_email, label)


cursor.execute("SELECT * FROM email_results")
print(cursor.fetchall())

conn.close()
