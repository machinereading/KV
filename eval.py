 # -*- coding: utf-8 -*-

from keras.models import load_model
import numpy as np
import json
from KG import KG_dataset
from scoring import normalize

class Ranking(object):
    def __init__(self, kg, model):
        self.kg = KG_dataset(kg)
        self.model = load_model(model)

    def ranked_list(self, triple, left_flag=True, filtered_flag=True, listlen=10):
        kg = self.kg
        model = self.model
        try:
            triple = [kg.word2id[x] for x in triple]
        except:
            print("no such entity or relation in the dataset")
            return [], 0

        sbj, rel, obj = triple
        scores = []
        triples = []

        # left_flag == True 면 obj 자리에 구멍을 뚫는 것을 의미함.
        # left_flag == False면 sbj 자리에 구멍을 뚫는 것을 의미함.
        if left_flag:
            for i in range(kg.num_entities):
                triples.append([sbj, rel, i])
        else:
            for i in range(kg.num_entities):
                triples.append([i, rel, obj])
        
        triples_ = [triples]
        
        scores = model.predict(triples_)
        triple_score_list = []

        for i in range(kg.num_entities):
            triple_score_list.append((triples[i], normalize(scores[i][0])))

        triple_score_list = sorted(triple_score_list, key = lambda x: x[1])
        triple_score_list.reverse()

        if filtered_flag:
            if left_flag:
                triple_score_list = [x for x in triple_score_list if x[0][2] not in kg.sbj_whole_triple_dict[(sbj, rel)] or x[0][2] == obj]
            else:
                triple_score_list = [x for x in triple_score_list if x[0][0] not in kg.obj_whole_triple_dict[(rel, obj)] or x[0][0] == sbj]

        rank = 0

        for i in range(len(triple_score_list)):
            if triple_score_list[i][0][0] == sbj and triple_score_list[i][0][2] == obj:
                rank = i+1

        word_score_list = []
        for i in range(len(triple_score_list)):
            triple = triple_score_list[i][0]
            word_triple = [kg.id2word[x] for x in triple]
            word_score_list.append((word_triple, triple_score_list[i][1]))

        if listlen == -1:
            return word_score_list, rank

        return word_score_list[:listlen], rank

if __name__ == "__main__":
    dataset = "data/KG/KBOX-iterative-T1/"
    model_name = "models/KBOX-iterative-T1.h5"
    Rank = Ranking(dataset, model_name)

    sample1 = [u'친일인명사전', u'developer', u'민족문제연구소']
    sample2 = [u'무서운_영화_4', u'language', u'영어']

    print(Rank.ranked_list(sample1))
    print(Rank.ranked_list(sample2))
    
