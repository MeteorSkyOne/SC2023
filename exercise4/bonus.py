import nltk
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import gutenberg
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

import string
import gensim
from gensim import corpora
import pyLDAvis.gensim_models

alice = gutenberg.raw('carroll-alice.txt')

alice = alice.lower()

alice = alice.translate(str.maketrans('', '', string.punctuation))

tokens = word_tokenize(alice)

lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stopwords.words('english')]

dictionary = corpora.Dictionary([tokens])
corpus = [dictionary.doc2bow([token]) for token in tokens]

lda_model = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)


vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis, 'lda.html')