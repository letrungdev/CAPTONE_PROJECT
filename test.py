# import spacy
# from spacy import displacy
#
# nlp = spacy.load('en_core_web_sm')
# introduction_text = 'hard disk is noisy'
# introduction_doc = nlp(introduction_text)
# displacy.serve(introduction_doc, style='dep')

#
# from nltk.corpus import wordnet
#
# synonyms = []
#
# for syn in wordnet.synsets("battery"):
#     print(syn.definition())
#     for l in syn.lemmas():
#         print(l.name())
#         synonyms.append(l.name())
#     print("\n\n")
#
# print(synonyms)
#
# import pandas as pd
# #
# #
# df = pd.read_csv("Data/amazon_reviews_us_Electronics_v1_00.tsv", error_bad_lines = False, sep='\t')


# df_laptop = df[df['product_title'].str.contains('laptop', na=False)]
#
# # Select only the columns you need for analysis
# df_laptop = df_laptop[['review_body', 'star_rating']]
#
# target_file = "Data/Train/laptop_train.csv"
# df_laptop['star_rating'] = df["star_rating"].astype('int')
#
# df_laptop.rename(
#     columns={"review_body": "Review", "star_rating": "Rating"},
#     inplace=True,
# )
# print(df_laptop.describe())
#
# df_laptop.to_csv(target_file, index=False)



from stanfordcorenlp import StanfordCoreNLP
import numpy as np
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp


# corenlp_path = "stanford-corenlp-4.5.1"
#
# MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
# noun_pos = ["NN", "NNS", "NNP"]
# adj_pos = ["JJ", "JJS", "JJR"]
#
#
#
#
# def SC(text):
#     nlp = StanfordCoreNLP(corenlp_path)
#     tokenize = nlp.word_tokenize(text)
#     pos = nlp.pos_tag(text)
#     dependency = nlp.dependency_parse(text)
#     nlp.close()
#     return tokenize, pos, dependency
#
#
# text = "set up was easy."
# print("Text: ", text, "\n")
# tokenize, pos, dependency = SC(text)
# print("Tokenize: ", tokenize, "\n")
# print("POS: ", pos, "\n")
# print("Dependency: ", dependency, "\n")


import gensim


embeddings_file = "word-embeddings/pruned.word2vec.txt"
model = gensim.models.KeyedVectors.load_word2vec_format(embeddings_file, binary=False)
neighbors = list(model.similar_by_word("price", topn=10))
print(neighbors)
