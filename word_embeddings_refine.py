import logging

import gensim
import numpy as np
import pandas as pd


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


def most_similar(word, w2v_model, weight_dict, top=10):
    sim_array = []
    word_array = []
    similar_words = w2v_model.most_similar(word, topn=top)
    i = 0
    for similar_word in similar_words:
        try:
            diff = weight_dict[word][similar_word[0]]
            sim_array.append([i, diff])
        except:
            sim_array.append([i, 0.0])
        word_array.append(similar_word[0])
        i += 1

    sim_array = np.array(sim_array)
    sort_index = sim_array[:, 1].argsort(0)
    new_array = sim_array[sort_index][::-1]

    ret_dict = {}
    for i in range(top):
        word = word_array[int(new_array[i][0])]
        ret_dict[word] = 1. / float(i+1.)

    return ret_dict


if __name__ == '__main__':
    top = 10
    max_iter = 100
    beta = 0.1
    gamma = 0.1
    valence_max = 9.0

    w2v_model_file = ""
    anew_file = ""
    logging.info("loading w2v_model...")
    w2v_model = gensim.models.KeyedVectors.load_word2vec_format(w2v_model_file, binary=False)
    embedding_dim = w2v_model.vector_size
    logging.info("loading lexicon...")
    anew = pd.read_table(anew_file, header=None, sep='\t', quoting=3)
    logging.info("lexicon loaded!")

    logging.info("prepare data...")
    anew_dict = {}
    vector_dict = {}
    for i in range(len(anew[0])):
        try:
            vector_dict[anew[0][i]] = w2v_model[anew[0][i]]
            anew_dict[anew[0][i]] = anew[1][i]
        except:
            continue

    logging.info("weight dictionary")
    weight_dict = {}
    for i in anew_dict.keys():
        for j in anew_dict.keys():
            weight = valence_max - abs(anew_dict[i] - anew_dict[j])
            update_dict(weight_dict, i, j, weight)

    logging.info("weight matrix")
    weight_matrix = np.zeros((len(anew_dict), len(anew_dict)))
    anew_dict_keys = list(anew_dict)
    for i in range(len(anew_dict_keys)):
        word_i = anew_dict_keys[i]
        sim_dict = most_similar(word_i, w2v_model, weight_dict, top=top)

        for j in range(len(anew_dict.keys())):
            word_j = anew_dict_keys[j]
            if word_j in sim_dict.keys():
                weight_matrix[i][j] = sim_dict[word_j]
                weight_matrix[j][i] = sim_dict[word_j]

    logging.info("vertex matrix")
    vertex_matrix = np.zeros((len(anew_dict.keys()), embedding_dim))
    for i in range(vertex_matrix.shape[0]):
        for j in range(vertex_matrix.shape[1]):
            vector = vector_dict[anew_dict_keys[i]]
            vertex_matrix[i, j] = vector[j]

    logging.info("weight matrix shape: " + str(weight_matrix.shape))
    logging.info("vertex matrix shape: " + str(vertex_matrix.shape))

    logging.info("starting refinement")
    origin_vertex_matrix = vertex_matrix
    pre_vertex_matrix = vertex_matrix
    pre_distance = 0.0
    diff = 1.0
    num_word = len(anew_dict.keys())

    for iteration in range(max_iter):
        pre_vertex_matrix = vertex_matrix.copy()
        for i in range(num_word):
            denominator = 0.0
            molecule = 0.0
            tmp_vertex = np.zeros((embedding_dim, ))
            weight_sum = 0.0
            for j in range(num_word):
                w_multi_v = weight_matrix[i, j] * pre_vertex_matrix
                weight_sum = weight_sum + weight_matrix[i, j]
                tmp_vertex = tmp_vertex + w_multi_v

            molecule = gamma * pre_vertex_matrix[i] + beta * tmp_vertex
            denominator = gamma + beta * weight_sum
            delta = molecule / denominator
            vertex_matrix[i] = delta

        distance = vertex_matrix - pre_vertex_matrix
        distanceT = distance.T
        value = np.dot(distance, distanceT)

        ec_distance = 0.0
        for i in range(embedding_dim):
            ec_distance = ec_distance + value[i, j]

        diff = abs(ec_distance - pre_distance)
        logging.info("cost: {}".format(diff))
        pre_distance = ec_distance

    refine_vector_file = w2v_model_file + ".refine"
    write_vector(refine_vector_file, w2v_model, vertex_matrix, anew_dict)

    