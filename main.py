from double_propagation import double_propagation
from prunning import prunning
from extract import extract
import pandas as pd


if __name__ == "__main__":
    review_file = "Data/Amazon_Mobile_Review.csv"
    extracted_target_file = "extracted/target.txt"
    extracted_opinion_file = "extracted/opinion.txt"
    stop_word_file = "stop_word/stop_words.txt"
    embeddings = "word-embeddings/pruned.word2vec.txt"

    df = pd.read_csv(review_file)
    reviews = df["Reviews"].tolist()[:10]

    # extract new target and opinion word to extracted folder
    double_propagation(reviews, extracted_target_file, extracted_opinion_file)
    # remove noise word
    aspect_dictionary = prunning(review_file, extracted_target_file, stop_word_file, embeddings)
    # extract target with opinion
    for review in reviews:
        extracted = extract(review_file, aspect_dictionary)
        print(extracted)

