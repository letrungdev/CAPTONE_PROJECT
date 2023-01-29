# import spacy
# from spacy import displacy
#
# nlp = spacy.load('en_core_web_sm')
# introduction_text = 'The phone has a good screen.'
# introduction_doc = nlp(introduction_text)
# displacy.serve(introduction_doc, style='dep')

# handle type mistakes
# import difflib
#
# print(len(difflib.get_close_matches('sound-effect', ['sjhjhj', 'aniddfgd', 'housfs', 'animsfsfation'])))


# import numpy as np
#
# s = [[1, 3], [2, 8], [3, 7]]
# s = np.array(s)
# sort_index = s[:, 1].argsort(0)
# new_array = s[sort_index][::-1]
# print(s)
# print(sort_index)
# print(new_array)

# from collections import Counter
# a = list(set(["fuck", "fuck", "ass"]))
# b = ["fuck"]
# other_target = list((Counter(a) - Counter(b)).elements())
# print(other_target)
# import gensim
#
# embeddings = "word-embeddings/pruned.word2vec.txt"
# model = gensim.models.KeyedVectors.load_word2vec_format(embeddings, binary=False)
# neighbors = list(model.similar_by_word("sound-effect", topn=3))
# print(neighbors)


# from difflib import SequenceMatcher
#
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()
#
# print(similar("sound-effect", "sound"))

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

