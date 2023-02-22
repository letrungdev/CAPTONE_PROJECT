from preprocessing import preprocessing
from nltk import sent_tokenize
from rule import extract_target_rule, extract_target_opinion, extract_target_polarity
from nltk.corpus import wordnet
import gensim
from collections import Counter
from difflib import SequenceMatcher
import json
from nltk.stem import WordNetLemmatizer
import pandas as pd


lemmatizer = WordNetLemmatizer()


def extract_aspect(reviews, target_file, opinion_file):
    for review in reviews:
        review = preprocessing(review)
        print(review)
        if len(review.split()) > 1:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                sentence = sentence.replace(".", "")
                for phrase in sentence.split(","):
                    targets = extract_target_rule(phrase, opinion_file)
                    print("Extracted targets", targets)
                    with open(target_file, "a+") as f:
                        for n in targets:
                            f.write(n + "\n")
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
    f = open(target_frequency_file)
    targets = json.load(f)
    model = gensim.models.KeyedVectors.load_word2vec_format(embeddings_file, binary=False)

    for n in range(40):
        target = max(targets, key=targets.get)
        try:
            top_targets.append(target)
            targets.pop(target)
        except:
            pass
    for word in top_targets:
        word = lemmatizer.lemmatize(word, pos="n")
        target_dictionary[word] = [word]

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
            a = similar(aspect, w)
            if a > 0.8 and w not in target_dictionary[aspect]:
                target_dictionary[aspect].append(w)
    with open(target_dictionary_file, 'w') as fp:
        json.dump(target_dictionary, fp, indent=4, ensure_ascii=False)


def target_opinion_dictionary(reviews, target_dictionary_file, target_opinion_file):
    target_opinion_dictionary = {}
    f = open(target_dictionary_file)
    target_dictionary = json.load(f)
    for aspect in target_dictionary:
        target_opinion_dictionary[aspect]["name"] = target_dictionary[aspect]
        target_opinion_dictionary[aspect]["opinion"] = []

    for review in reviews:
        review = preprocessing(review)
        print(review)
        if len(review.split()) > 1:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                sentence = sentence.replace(".", "")
                for phrase in sentence.split(","):
                    extracted = extract_target_opinion(phrase, target_dictionary)
                    for n in extracted:
                        if extracted[n] not in target_opinion_dictionary[n]["opinion"]:
                            target_opinion_dictionary[n]["opinion"].append(extracted[n])

    with open(target_opinion_file, 'w') as fp:
        json.dump(target_opinion_dictionary, fp, indent=4, ensure_ascii=False)


def target_sentiment_polarity_dictionary(train_file, target_opinion_file, dictionary_file):
    dictionary = {}
    polarity_process = {}
    df = pd.read_csv(train_file)
    f = open(target_opinion_file)
    target_opinion = json.load(f)

    for i, row in df.iterrows():
        review = row['review']
        review = preprocessing(review)
        print(review)
        if len(review.split()) > 1:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                sentence = sentence.replace(".", "")
                for phrase in sentence.split(","):
                    extracted = extract_target_opinion(phrase, target_dictionary)

                    # for n in extracted:
                    #     for
                    #     if extracted[n] not in target_opinion_dictionary[n]["opinion"]:
                    #         target_opinion_dictionary[n]["opinion"].append(extracted[n])



        rating = row['rating']



    for aspect in target_opinion:
        # Loop through each sentiment word for the aspect
        for sentiment_word in target_opinion[aspect]["opinion"]:
            # Initialize counts for each rating score
            positive_count = 0
            neutral_count = 0
            negative_count = 0
            total_count = 0

            # Loop through each review in the dataset
            for i, row in df.iterrows():
                # Extract the review and rating for the row
                review = row['review']
                rating = row['rating']

                # Check if the sentiment word appears in the review
                if word in review:
                    # Update the count for the corresponding rating score
                    if rating in [4, 5]:
                        positive_count += 1
                    elif rating == 3:
                        neutral_count += 1
                    elif rating in [1, 2]:
                        negative_count += 1
                    total_count += 1

            # Determine the polarity of the sentiment word based on the counts
            if total_count > 0:
                positive_ratio = positive_count / total_count
                neutral_ratio = neutral_count / total_count
                negative_ratio = negative_count / total_count
                if positive_ratio > neutral_ratio and positive_ratio > negative_ratio:
                    polarity = 'positive'
                elif neutral_ratio > positive_ratio and neutral_ratio > negative_ratio:
                    polarity = 'neutral'
                else:
                    polarity = 'negative'
            else:
                polarity = 'unknown'

            # Add the sentiment word and its polarity to the polarities dictionary
            polarities[word] = polarity


