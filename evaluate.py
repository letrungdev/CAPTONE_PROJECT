import pandas as pd
from rule import extract_target_polarity
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
        extracted_aspects = extract_target_polarity(row['Sentence'], dictionary_file)

        # Loop through each extracted aspect and its associated sentiment words
        for aspect in extracted_aspects:
            sentiment_polarity = extracted_aspects[aspect]
            if aspect == row['Aspect Term']:
                accuracy_target += 1
            if sentiment_polarity == row['polarity']:
                accuracy_polarity += 1

    print("Total records: ", total_record)
    print("Number of correct extracted targets: {}, percent: {}".format(accuracy_target, accuracy_target/total_record))
    print("Number of correct sentiment polarity: {}, percent: {}".format(accuracy_polarity, accuracy_polarity / total_record))