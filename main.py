from double_propagation import double_propagation
from prunning import prunning
from opinion_for_aspect import opinion_for_aspect
from extract import extract
import pandas as pd


if __name__ == "__main__":
    review_file = "Data/Amazon_Mobile_Review.csv"
    extracted_target_file = "extracted/target.txt"
    extracted_opinion_file = "extracted/opinion.txt"
    stop_word_file = "stop_word/stop_words.txt"
    embeddings = "word-embeddings/pruned.word2vec.txt"
    aspect_dictionary_file = "target_dictionary.json"

    df = pd.read_csv(review_file)
    reviews = df["Reviews"].tolist()

    # extract new target and opinion word to extracted folder
    # double_propagation(reviews, extracted_target_file, extracted_opinion_file)

    # prunning(extracted_target_file, stop_word_file, embeddings)

    # extract target with opinion
    opinion_for_aspect(reviews[:10], aspect_dictionary_file)



