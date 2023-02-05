# import spacy
# from spacy import displacy
#
# nlp = spacy.load('en_core_web_sm')
# introduction_text = 'The phone has a good screen.'
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


from rule import SC
import numpy as np


noun_pos = ["NN", "NNS", "NNP"]
MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
adj_pos = ["JJ", "JJS", "JJR"]

sentence = "this is good screen"
print(sentence)
tokenize, pos, dependency = SC(sentence)
tokenize = np.array(tokenize)
for index, i in enumerate(pos):
    if i[1] in noun_pos:
        for j in dependency:
            if j[0] in MR:
                if j[1] == (index + 1):
                    relate_word_position = j[2]
                    print(relate_word_position)
                    if pos[relate_word_position - 1][1] in adj_pos:
                        o = tokenize[relate_word_position - 1]
                        print(o)
