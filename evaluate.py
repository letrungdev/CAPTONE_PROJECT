import pandas as pd
from rule import extract_target_polarity_rule
import json


def evaluate(evaluate_file, dictionary_file):
    total_record = 0
    accuracy_target = 0
    accuracy_polarity = 0

    aspect_dict = {}
    # Load the CSV file into a Pandas DataFrame
    data = pd.read_csv(evaluate_file)

    for index, row in data.iterrows():
        total_record += 1
        # Extract aspects and sentiment words from the review
        extracted_aspects = extract_target_polarity_rule(row['Sentence'], dictionary_file)

        # Loop through each extracted aspect and its associated sentiment words
        for aspect in extracted_aspects:
            sentiment_polarity = extracted_aspects[aspect]
            if aspect == row['Aspect Term']:
                accuracy_target += 1
            if sentiment_polarity == row['polarity']:
                accuracy_polarity += 1

    print("Total records: ", total_record)
    print("Number of correct extracted targets: {}, percent: {}".format(accuracy_target, accuracy_target/total_record))


def evaluate_aspect_polarity_extraction(evaluate_file, dictionary_file):
    with open(dictionary_file) as f:
        dictionary = json.load(f)

    df = pd.read_csv(evaluate_file)

    tp = 0
    fp = 0
    fn = 0
    for i, row in df.iterrows():
        sentence = row["Sentence"]
        aspect = row["Aspect Term"]
        polarity = row["polarity"]
        print(i, sentence, aspect, polarity)
        extracted_aspect_polarity = extract_target_polarity_rule(sentence, dictionary)
        print(extracted_aspect_polarity)
        # Check if the extracted aspect and polarity match the true values
        if aspect in extracted_aspect_polarity and polarity == extracted_aspect_polarity[aspect]:
            tp += 1
        elif aspect not in extracted_aspect_polarity:
            fn += 1
            fp += 1
        else:
            fp += 1

        print(tp, fp, fn)
    # Calculate accuracy and recall
    accuracy = tp / (tp + fp)
    recall = tp / (tp + fn)

    print("Aspect Extract Accuracy: ", accuracy)
    print("Aspect Extract Recall: ", recall)
    return accuracy, recall



