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
# print(difflib.get_close_matches('sound-effect', ['sound effects', 'animal', 'house', 'animation']))


import numpy as np

s = [[1, 3], [2, 8], [3, 7]]
s = np.array(s)
sort_index = s[:, 1].argsort(0)
new_array = s[sort_index][::-1]
print(s)
print(sort_index)
print(new_array)