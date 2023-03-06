import pandas as pd
from process import extract_aspect, target_frequency, target_dictionary, create_dictionary
from evaluate import evaluate, evaluate_aspect_polarity_extraction


if __name__ == "__main__":
    # embeddings_file = "word-embeddings/pruned.word2vec.txt"

    # Restaurant
    # train_file = "Data/Train/restaurant_train.csv"
    # extract_target_file = "extracted/target.txt"
    # opinion_file = "opinion-lexicon/opinion.txt"
    # stop_word_file = "stop_word/stop_words.txt"
    # target_frequency_file = "process/target_frequency.json"
    # target_dictionary_file = "process/target_dictionary.json"
    # dictionary_file = "process/dictionary.json"
    # embeddings_file = "word-embeddings/pruned.word2vec.txt"
    # evaluate_file = "Data/Evaluate/Restaurants_Train_v2.csv"


    # laptop
    train_file = "Data/Train/laptop_train.csv"
    extract_target_file = "extracted/laptop_aspect.txt"
    opinion_file = "opinion-lexicon/opinion.txt"
    stop_word_file = "stop_word/stop_words.txt"
    target_frequency_file = "process/laptop_aspect_frequency.json"
    target_dictionary_file = "process/laptop_aspect_dictionary.json"
    dictionary_file = "process/laptop_dictionary.json"
    evaluate_file = "Data/evaluate/laptop_evaluate.csv"

    # read train file
    # df = pd.read_csv(train_file, encoding = 'unicode_escape')
    # reviews = df["Review"].tolist()

    # get sentiment word list
    # opinion_words = set(open(opinion_file).read().split())

    # extract aspect to target file
    # extract_aspect(reviews, extract_target_file, opinion_words)

    # creat aspect dictionary
    # target_frequency = target_frequency(extract_target_file, stop_word_file, target_frequency_file)
    # target_dictionary = target_dictionary(target_frequency_file, embeddings_file, target_dictionary_file)

    # creat aspect opinion dictionary
    # create_dictionary(small_train_file, target_dictionary_file, dictionary_file)

    evaluate(evaluate_file, dictionary_file)

