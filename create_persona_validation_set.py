import os
import cPickle
import numpy as np
from tensorflow.contrib import learn
from pathlib import Path
import time
from shutil import copyfile
from data_helpers import parse_persona_chat_dataset, process_train_file, make_embedding_matrix, load_word2vec
import random

if __name__ == '__main__':
    raw_data_dir = "data/validation_raw_personachat"
    processed_data_dir = processed_train_dir = "data/personachat/validation"
    fquery_train, freply_train = parse_persona_chat_dataset(raw_data_dir, processed_data_dir, "valid")
    freply = os.path.join(processed_data_dir, freply_train)
    fquery = os.path.join(processed_data_dir, fquery_train)

    copyfile(freply, freply + ".true.sub")
    reply_true = open(freply).readlines()
    random.shuffle(reply_true)
    open(freply + ".sub", "w+").writelines(reply_true)
    copyfile(fquery, fquery + ".sub")

    query_max_length, reply_max_length = [20, 30]
    # Path to word2vec weights
    fqword2vec = 'GoogleNews-vectors-negative300.txt'
    frword2vec = 'GoogleNews-vectors-negative300.txt'

    print("Processing training files into vocab and embedding files")

    #make sure embed and vocab file paths are correct
    raw_data_dir = "./data"
    process_train_file(processed_train_dir, fquery_train, query_max_length)
    process_train_file(processed_train_dir, freply_train, reply_max_length)

    fqvocab = '%s.vocab%d'%(fquery_train, query_max_length)
    frvocab = '%s.vocab%d'%(freply_train, reply_max_length)

    word2vec, vec_dim, _ = load_word2vec(raw_data_dir, fqword2vec)
    make_embedding_matrix(processed_train_dir, fquery_train, word2vec, vec_dim, fqvocab)

    word2vec, vec_dim, _ = load_word2vec(raw_data_dir, frword2vec)
    make_embedding_matrix(processed_train_dir, freply_train, word2vec, vec_dim, frvocab)
    pass
