from nltk.corpus import wordnet
import gensim
from collections import Counter
from difflib import SequenceMatcher
import json


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def expand_target(other_targets, top_targets, embeddings):
    target_expand = {}
    model = gensim.models.KeyedVectors.load_word2vec_format(embeddings, binary=False)
    for word in top_targets:
        target_expand[word] = [word]

    # expand by similarity from word2vec
    # for word in top_targets:
    #     try:
    #         neighbors = list(model.similar_by_word(word, topn=10))
    #         if len(neighbors) > 0:
    #             for neighbor in neighbors:
    #                 if neighbor[0] in other_targets:
    #                     print(neighbor[0])
    #                     target_expand[word].append(neighbor[0])
    #     except:
    #         pass

        # similar typing targets
        for w in other_targets:
            a = similar(word, w)
            if a > 0.8 and w not in target_expand[word]:
                target_expand[word].append(w)

    return target_expand


def prunning(extracted_target_file, stop_word_file, embeddings):
    top_target = []
    f = open(extracted_target_file)
    g = open(stop_word_file)
    targets = Counter([word.replace("\n", "") for word in f.readlines()])
    print(targets)

    targets = {i:targets[i] for i in targets if i not in g.read()}
    targets = dict(sorted(targets.items(), key=lambda x: x[1], reverse=True))
    with open('process/target_count.json', 'w') as f:
        json.dump(targets, f, indent=4, ensure_ascii=False)

    for n in range(30):
        target = max(targets, key=targets.get)
        try:
            top_target.append(target)
            targets.pop(target)
        except:
            pass

    other_targets = list(targets.keys())
    expand = expand_target(other_targets, top_target, embeddings)
    print(expand)
    with open('process/target_dictionary.json', 'w') as fp:
        json.dump(expand, fp, indent=4, ensure_ascii=False)

