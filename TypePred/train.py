import re
import json
import numpy as np

def strTrim(str):
    trimmed = re.sub('\?|\.|\,|\!|\;|\:|\"|\—|\(|\)', '', str)
    if len(trimmed) != len(str):
        return trimmed, 1
    return str, 0

def trimModel(bigram, trigram):
    print("Trimming Bigram model...")
    bigram_k = list(bigram.keys())
    for key in bigram_k:
        keys = list(bigram[key].keys())
        vals = list(bigram[key].values())
        word1, word2, word3 = getWords(keys, vals)
        if (word1 == ''):
            bigram[key] = {}
        elif (word2 == ''):
            bigram[key] = {word1: 300}
        elif (word3 == ''):
            bigram[key] = {word1: 300, word2: 200}
        else:
            bigram[key] = {word1: 300, word2: 200, word3: 100}
    trigram_k = list(trigram.keys())
    print("Trimming Trigram model...")
    for key in trigram_k:
        keys = list(trigram[key].keys())
        vals = list(trigram[key].values())
        word1, word2, word3 = getWords(keys, vals)
        if (word1 == ''):
            trigram[key] = {}
        elif (word2 == ''):
            trigram[key] = {word1: 300}
        elif (word3 == ''):
            trigram[key] = {word1: 300, word2: 200}
        else:
            trigram[key] = {word1: 300, word2: 200, word3: 100}
    print("Models trimmed.")

def getWords(keys, vals):
    word2 = ''
    word3 = ''
    word1 = keys[np.argmax(vals)]
    vals[np.argmax(vals)] = 0
    if len(keys) > 1:
        word2 = keys[np.argmax(vals)]
        vals[np.argmax(vals)] = 0
    if len(keys) > 2:
        word3 = keys[np.argmax(vals)]
        vals[np.argmax(vals)] = 0
    return word1, word2, word3

def main():
    print("Loading training data...")

    with open('input.txt', "r", encoding="utf8") as word_list:
        words = word_list.read().split()

    for i, w in enumerate(words):
        words[i] = strTrim(w)[0]

    total_len = len(words)
    total_len_d = total_len * 2

    trigram_result = {}
    for i in range(len(words) - 2):
        if (i % 10000 == 0):
            print("Training", i,"words out of", total_len_d, "words", end = "\r")
        w1w2 = words[i] + " " + words[i + 1]
        if w1w2 not in trigram_result:
            trigram_result[w1w2] = {words[i + 2]: 1}
        else:
            inner_dict = trigram_result[w1w2]
            if words[i + 2] not in inner_dict:
                inner_dict[words[i + 2]] = 1
            else:
                inner_dict[words[i + 2]] += 1
    bigram_result = {}
    for i in range(len(words) - 1):
        if (i % 10000 == 0):
            print("Training", i + total_len,"words out of", total_len_d, "words", end = "\r")
        w1 = words[i]
        if w1 not in bigram_result:
            bigram_result[w1] = {words[i + 1]: 1}
        else:
            inner_dict = bigram_result[w1]
            if words[i + 1] not in inner_dict:
                inner_dict[words[i + 1]] = 1
            else:
                inner_dict[words[i + 1]] += 1

    print("Training", total_len_d,"words out of", total_len_d, "words")
    print("Training complete!")

    trimModel(bigram_result, trigram_result)

    print("Saving Bigram model...")
    with open("bigram_model.json", "w") as outfile:
        json.dump(bigram_result, outfile)
    print("Bigram model saved!")
    print("Saving Trigram model...")
    with open("trigram_model.json", "w") as outfile:
        json.dump(trigram_result, outfile)
    print("Trigram model saved!")

if __name__ == "__main__":
    main()
