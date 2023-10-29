import nltk
import matplotlib.pyplot as plt
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

with open('moby_dick.txt', 'r', encoding='utf-8') as f:
    moby_dick_text = f.read()

tokens = word_tokenize(moby_dick_text)

stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

pos_tags = pos_tag(filtered_tokens)

pos_counter = Counter(tag for word, tag in pos_tags)
most_common_pos = pos_counter.most_common(5)
print("5 Most Common Parts of Speech and Their Counts:")
for tag, count in most_common_pos:
    print(f"{tag}: {count}")

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    tag = tag[0].upper()
    tag_dict = {"J": "a", "N": "n", "V": "v", "R": "r"}
    return tag_dict.get(tag, "n")

lemmatized_tokens = [(lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)), tag) for word, tag in pos_tags[:20] if tag[0].isalpha()]
print("Top 20 Lemmatized Tokens:")
print(lemmatized_tokens)

plt.figure(figsize=(10, 6))
plt.bar(pos_counter.keys(), pos_counter.values())
plt.xlabel('Parts of Speech')
plt.ylabel('Frequency')
plt.title('Frequency Distribution of Parts of Speech')
plt.xticks(rotation=45)
plt.savefig('pos_frequency_distribution.png')
plt.show()

sia = SentimentIntensityAnalyzer()

sentiment_scores = sia.polarity_scores(moby_dick_text)
print(f"Sentiment Scores: {sentiment_scores}")

if sentiment_scores['compound'] > 0.05:
    print("The overall text sentiment is positive.")
elif sentiment_scores['compound'] < -0.05:
    print("The overall text sentiment is negative.")
else:
    print("The overall text sentiment is neutral.")
