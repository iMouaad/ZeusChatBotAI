import nltk
# nltk.download()
import tensorflow
import os
import tflearn
import random
import numpy
import json
import pickle
import pandas
from nltk.stem.lancaster import LancasterStemmer
from difflib import get_close_matches


stemmer = LancasterStemmer()
intents_filepath = 'C:\\chatbot\\intents.json'
dict_path = 'C:\\chatbot\\close_matches.txt'

with open(intents_filepath, encoding='utf-8') as file:
    data = json.load(file)

try:
    # uncomment this to retrain the model or delete the old model
    #retrain
    print("executing except")
    with open("data.pickle", "rb") as file:
        words, labels, training, output = pickle.load(file)

except:
    words = []
    labels = []
    docsX = []
    docsY = []
    dic_file_content = ''
    if os.path.exists("data.json"):
        os.remove(dict_path)
    dict_file = open("close_matches.txt", "w")

    for intent in data["intents"]:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docsX.append(wrds)
            docsY.append(intent['tag'])
            dic_file_content += pattern
            dic_file_content += ","

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    dic_file_content = dic_file_content[:-1] # to remove last , comma
    dict_file.write(dic_file_content)
    dict_file.close()
    words = [stemmer.stem(w.lower()) for w in words if w not in '?']
    # remove all the duplicates words
    words = sorted(list(set(words)))
    labels = sorted(labels)

    # neural network only understands numbers we need to convert them 'bag of words'
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docsX):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docsY[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)

# tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    # uncomment this to retrain the model or delete the old model
    #retrain
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


data_bank = list(pandas.read_csv(dict_path))


def chat(user_input):
    global responses
    results = model.predict([bag_of_words(user_input, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.7:
        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
        return random.choice(responses)
    else:
        return "No answer in my database yet."


def get_close_match(phrase):
    if phrase not in data_bank:
        suggestions = get_close_matches(phrase, data_bank, 1)
        # print("not found, close matches is: ", suggestion)
        if suggestions:
            phrase = suggestions[0]
        print("suggestions is:", suggestions)
    return phrase


while True:
    client_input = input("You: ")
    valid_input = get_close_match(client_input)
    print("input now:", valid_input)
    answer = chat(valid_input.lower())
    print("bot:", answer)


'''
def zeus_response(string):
    valid_input = get_close_match(string)
    answer = chat(valid_input.lower())
    return answer
'''












