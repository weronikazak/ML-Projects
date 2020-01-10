import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer #onvert a collection of raw documents to a matrix of TF-IDF features
from sklearn.metrics.pairwise import cosine_similarity #This will be used to find the similarity between words entered by the user and the words in the corpus

f = open('chatbot.txt', 'r', errors='ignore')

raw = f.read()
raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw) # converts to list of sentences
word_tokens = nltk.sent_tokenize(raw) # converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "hey", "greetings", "sup", "whassup")
GREETING_RESPONDES = ("hi", "hey", "*nods*", "hi there", "hello", "I am glad youre talking to me")

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONDES)

def response(user_response):
    robo_response = ""
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words="english")
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfisf = flat[-2]

    if (req_tfisf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response

flag = True
print("ROBO: My name is Robo. I will answer your quesries about Chatbots. If you want to exit type 'Bye'!")

while (flag==True):
    user_response = input()
    user_response = user_response.lower()
    if (user_response != "bye"):
        if (user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("ROBO: you're welcome")
        else:
            if (greeting(user_response)!=None):
                print("ROBO: " + greeting(user_response))
            else:
                print("ROBO: ", end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("ROBO: Bye! Take care")