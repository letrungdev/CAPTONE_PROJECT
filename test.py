# import spacy
# from spacy import displacy
#
# nlp = spacy.load('en_core_web_sm')
# introduction_text = 'Customization on Mac is impossible'
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





# import requests
# from bs4 import BeautifulSoup
#
# word = "hard disk"
# url = "https://en.wikipedia.org/wiki/hard disk"
# page = requests.get(url)
# soup = BeautifulSoup(page.text, "html.parser")
# a = soup.find(class_="mw-page-title-main").text.lower()
# print(a)

for n in range(4):
    print(n)