import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer

# Load chat log
with open("chat.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Separate messages
user_messages = []
ai_messages = []

for line in lines:
    if line.startswith("User:"):
        user_msg = line.replace("User:", "").strip()
        user_messages.append(user_msg)
    elif line.startswith("AI:"):
        ai_msg = line.replace("AI:", "").strip()
        ai_messages.append(ai_msg)

# Count stats
total_messages = len(user_messages) + len(ai_messages)

# Preprocess messages for TF-IDF
def preprocess(text):
    text = text.lower()
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    return text

all_messages = user_messages + ai_messages
processed_messages = [preprocess(msg) for msg in all_messages]

# TF-IDF Keyword Extraction
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(processed_messages)
tfidf_scores = tfidf_matrix.sum(axis=0).A1
feature_names = vectorizer.get_feature_names_out()

# Get top 5 keywords
tfidf_dict = dict(zip(feature_names, tfidf_scores))
sorted_keywords = sorted(tfidf_dict.items(), key=lambda x: x[1], reverse=True)
top_keywords = [word for word, score in sorted_keywords[:5]]

# Print summary
print("\nSummary:")
print(f"- The conversation had {total_messages} exchanges.")
print(f"- User sent {len(user_messages)} messages, AI responded with {len(ai_messages)} messages.")
print(f"- Most important keywords (TF-IDF): {', '.join(top_keywords)}")
