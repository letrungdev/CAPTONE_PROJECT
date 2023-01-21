import gensim


def update_dict(target_dict, key_a, key_b, val):
    if key_a in target_dict:
        target_dict[key_a].update({key_b: val})
    else:
        target_dict.update({key_a:{key_b: val}})


def write_vector(file_name, w2v_model, vertex_matrix, anew_dict):
    with open(file_name, 'w', encoding='utf8') as f:
        for i in range(len(anew_dict.keys())):
            word = anew_dict.keys()[i]
            vec = vertex_matrix[i]
            f.write('%s %s\n' % (word, ' '.join('%f' % val for val in vec)))
        for word in w2v_model.vocab:
            if word not in anew_dict.keys():
                vec = w2v_model[word]
                f.write('%s %s\n' % (word, ' '.join('%f' % val for val in vec)))


def most_similar(word, w2vmodel, anew_dict, weight_dict, t)