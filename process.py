from preprocessing import preprocessing
from nltk import sent_tokenize
from rule import extract_target_rule, extract_target_opinion_rule, extract_target_polarity_rule
from nltk.corpus import wordnet
import gensim
from collections import Counter
from difflib import SequenceMatcher
import json
from nltk.stem import WordNetLemmatizer
import pandas as pd
import heapq
from collections import defaultdict


lemmatizer = WordNetLemmatizer()


def extract_aspect(reviews, target_file, opinion_words):
    for review in reviews:
        review = preprocessing(review)
        print(review)
        if len(review.split()) > 1:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                sentence = sentence.replace(".", "")
                for phrase in sentence.split(","):
                    targets = extract_target_rule(phrase, opinion_words)
                    print("Extracted targets", targets)
                    with open(target_file, "a+") as f:
                        for n in targets:
                            try:
                                f.write(n + "\n")
                            except:
                                pass
                    f.close()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def target_frequency(extracted_target_file, stop_word_file, target_frequency_file):
    f = open(extracted_target_file)
    g = open(stop_word_file)
    targets = Counter([word.replace("\n", "") for word in f.readlines()])
    targets = {i:targets[i] for i in targets if i not in g.read()}
    targets = dict(sorted(targets.items(), key=lambda x: x[1], reverse=True))
    with open(target_frequency_file, 'w') as f:
        json.dump(targets, f, indent=4, ensure_ascii=False)


def target_dictionary(target_frequency_file, embeddings_file, target_dictionary_file):
    target_dictionary = {}
    top_targets = []
    top_n = 150
    f = open(target_frequency_file)
    targets = json.load(f)
    model = gensim.models.KeyedVectors.load_word2vec_format(embeddings_file, binary=False)
    top_targets = heapq.nlargest(top_n, targets, key=targets.get)
    for target in top_targets:
        lemma_word = lemmatizer.lemmatize(target, pos="n")
        if lemma_word not in target_dictionary:
            if lemma_word == target:
                target_dictionary[lemma_word] = [lemma_word]
            else:
                target_dictionary[lemma_word] = [lemma_word, target]
        else:
            if lemma_word != target and target not in target_dictionary[lemma_word]:
                target_dictionary[lemma_word].append(target)

    # expand by similarity from word2vec
    # for word in top_targets:
    #     try:
    #         neighbors = list(model.similar_by_word(word, topn=10))
    #         if len(neighbors) > 0:
    #             for neighbor in neighbors:
    #                 if neighbor[0] in other_targets:
    #                     print(neighbor[0])
    #                     target_expand[word].append(neighbor[0])
    #     except:
    #         pass

    # similar typing targets

    for w in targets:
        for aspect in target_dictionary:
            if any(similar(w, aspect_name) > 0.8 for aspect_name in target_dictionary[aspect]):
                if w not in target_dictionary[aspect]:
                    target_dictionary[aspect].append(w)

    with open(target_dictionary_file, 'w') as fp:
        json.dump(target_dictionary, fp, indent=4, ensure_ascii=False)


def create_dictionary_ver1(train_file, target_dictionary_file, dictionary_file):
    df = pd.read_csv(train_file)
    target_dictionary = json.load(open(target_dictionary_file))
    dictionary = {aspect: {"name": target_dictionary[aspect], "opinion": {"positive": [], "neutral": [], "negative": []}} for aspect in target_dictionary}
    sentiment_polarity_process = {}
    for i, row in df.iterrows():
        review, rating = preprocessing(row["Review"]), row["Rating"]
        for sentence in sent_tokenize(review):
            sentence = sentence.replace(".", "")
            extracted = extract_target_opinion_rule(sentence, target_dictionary)
            if not extracted:
                continue
            for n in extracted:
                sentiment_polarity_process.setdefault(n, {}).setdefault(extracted[n], {"positive": 0, "neutral": 0, "negative": 0})
            polarity = ""
            if rating in [4, 5]: polarity = "positive"
            elif rating == 3: polarity = "neutral"
            elif rating in [1, 2]: polarity = "negative"
            for n in extracted:
                sentiment_polarity_process[n][extracted[n]][polarity] += 1
    for aspect in sentiment_polarity_process:
        for sentiment_word in sentiment_polarity_process[aspect]:
            polarity = max(sentiment_polarity_process[aspect][sentiment_word], key=sentiment_polarity_process[aspect][sentiment_word].get)
            if sentiment_word not in dictionary[aspect]["opinion"][polarity]:
                dictionary[aspect]["opinion"][polarity].append(sentiment_word)

    with open(dictionary_file, "w") as f:
        json.dump(dictionary, f, indent=4)


def create_dictionary(train_file, target_dictionary_file, dictionary_file):
    dictionary = {}
    sentiment_polarity_process = {}
    df = pd.read_csv(train_file, encoding='unicode_escape')
    f = open(target_dictionary_file)
    target_dictionary = json.load(f)
    for aspect in target_dictionary:
        dictionary[aspect] = {}
        dictionary[aspect]["name"] = target_dictionary[aspect]
        dictionary[aspect]["opinion"] = {
            "positive": [],
            "neutral": [],
            "negative": []
        }
    for i, row in df.iterrows():
        print(i+1)
        review = row["Review"]
        rating = row["Rating"]
        review = preprocessing(review)
        print(review, rating)
        sentences = sent_tokenize(str(review))
        for sentence in sentences:
            sentence = sentence.replace(".", "")
            extracted = extract_target_opinion_rule(sentence, target_dictionary)
            if extracted == {}:
                continue
            print(extracted)
            for n in extracted:
                if sentiment_polarity_process.get(n) is None:
                    sentiment_polarity_process[n] = {}
                if sentiment_polarity_process[n].get(extracted[n]) is None:
                    sentiment_polarity_process[n][extracted[n]] = {
                        "positive": 0,
                        "neutral": 0,
                        "negative": 0
                    }
            if rating in [4, 5]:
                for n in extracted:
                    sentiment_polarity_process[n][extracted[n]]["positive"] += 1
            elif rating == 3:
                for n in extracted:
                    sentiment_polarity_process[n][extracted[n]]["neutral"] += 1
            elif rating in [1, 2]:
                for n in extracted:
                    sentiment_polarity_process[n][extracted[n]]["negative"] += 1
    with open("process/sentiment_polarity_proces.json", 'w') as fp:
        json.dump(sentiment_polarity_process, fp, indent=4, ensure_ascii=False)

    print(sentiment_polarity_process)
    for aspect in sentiment_polarity_process:
        for sentiment_word in sentiment_polarity_process[aspect]:
            polartity = sentiment_polarity_process[aspect][sentiment_word]
            if polartity["positive"] > polartity["neutral"] and polartity["positive"] > polartity["negative"]:
                if dictionary[aspect]["opinion"]["positive"] is None:
                    dictionary[aspect]["opinion"]["positive"] = [sentiment_word]
                elif sentiment_word not in dictionary[aspect]["opinion"]["positive"]:
                    dictionary[aspect]["opinion"]["positive"].append(sentiment_word)
            elif polartity["neutral"] > polartity["positive"] and polartity["neutral"] > polartity["negative"]:
                if dictionary[aspect]["opinion"]["neutral"] is None:
                    dictionary[aspect]["opinion"]["neutral"] = [sentiment_word]
                elif sentiment_word not in dictionary[aspect]['opinion']['positive']:
                    dictionary[aspect]["opinion"]["neutral"].append(sentiment_word)
            elif polartity["negative"] > polartity["positive"] and polartity["negative"] > polartity["neutral"]:
                if dictionary[aspect]["opinion"]["negative"] is None:
                    dictionary[aspect]["opinion"]["negative"] = [sentiment_word]
                elif sentiment_word not in dictionary[aspect]["opinion"]["negative"]:
                    dictionary[aspect]["opinion"]["negative"].append(sentiment_word)

    with open(dictionary_file, 'w') as fp:
        json.dump(dictionary, fp, indent=4, ensure_ascii=False)


