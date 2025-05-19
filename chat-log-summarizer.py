import re
from collections import Counter
import string

try:
    from nltk.corpus import stopwords
    nltk_stopwords = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    nltk_stopwords = set(nltk.corpus.stopwords.words('english'))

#CONFIG
CHAT_FILE = 'chat.txt'

#LOAD CHAT
with open(CHAT_FILE, 'r', encoding='utf-8') as file:
    lines = file.readlines()

#PARSE MESSAGES
user_messages = []
ai_messages = []

for line in lines:
    line = line.strip()
    if line.startswith("User:"):
        user_messages.append(line[len("User:"):].strip())
    elif line.startswith("AI:"):
        ai_messages.append(line[len("AI:"):].strip())

total_messages = len(user_messages) + len(ai_messages)

#KEYWORD ANALYSIS
def extract_keywords(messages):
    words = []
    for msg in messages:
        tokens = msg.lower().translate(str.maketrans('', '', string.punctuation)).split()
        filtered = [w for w in tokens if w not in nltk_stopwords]
        words.extend(filtered)
    return Counter(words).most_common(5)

combined_messages = user_messages + ai_messages
top_keywords = extract_keywords(combined_messages)

#GENERATE SUMMARY
print("\nSummary:")
print(f"- The conversation had {total_messages} exchanges.")
print(f"- User sent {len(user_messages)} messages, AI responded with {len(ai_messages)} messages.")
print("- Most common keywords:", ', '.join([kw for kw, _ in top_keywords]))