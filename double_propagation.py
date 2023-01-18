import rule
import pandas as pd
from nltk.tokenize import sent_tokenize


file = "Data/amazon_reviews.csv"
opinion_file = "opinion.txt"
target_file = "target.txt"


def seed_opinion():
    list_opinion = []
    positive_opinion_fp = "opinion-lexicon/positive-words.txt"
    negative_opinion_fp = "opinion-lexicon/negative-words.txt"
    f = open(positive_opinion_fp)
    g = open(negative_opinion_fp)
    for word in f.readlines()[30:]:
        list_opinion.append(word.replace("\n", ""))
    for word in g.readlines()[30:]:
        list_opinion.append(word.replace("\n", ""))
    f.close()
    g.close()
    list_opinion = list(set(list_opinion))
    with open(opinion_file, "w") as f:
        for n in list_opinion:
            f.write(n + "\n")
    f.close()


f = open("target.txt")
g = open("opinion.txt")


def double_propagation(file):
    df = pd.read_csv(file)
    reviews = df["reviewText"].tolist()[:10]
    for review in reviews:
        sentences = sent_tokenize(str(review))
        for sentence in sentences:
            rule.rule1(sentence, opinion_file)
            rule.rule4(sentence, opinion_file)

    for review in reviews:
        sentences = sent_tokenize(str(review))
        for sentence in sentences:
            rule.rule3(sentence, target_file)
            rule.rule2(sentence, target_file, opinion_file)


# seed_opinion()
double_propagation(file)





