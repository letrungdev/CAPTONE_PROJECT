import pandas as pd
from process import extract_aspect, target_frequency, target_dictionary

if __name__ == "__main__":
    train_file = "Data/Train/restaurant_train.csv"
    extract_target_file = "extracted/target.txt"
    opinion_file = "opinion-lexicon/opinion.txt"
    stop_word_file = "stop_word/stop_words.txt"
    target_frequency_file = "process/target_frequency.json"
    target_dictionary_file = "process/target_dictionary.json"
    embeddings_file = "word-embeddings/pruned.word2vec.txt"
    evaluate_file = "Data/Restaurants_Train_v2.csv"

    df = pd.read_csv(train_file)

    # reviews = df["Review"].tolist()
    # extract_aspect(reviews, extract_target_file, opinion_file)

    # target_frequency(extract_target_file, stop_word_file, target_frequency_file)

    target_dictionary(target_frequency_file, embeddings_file, target_dictionary_file)




