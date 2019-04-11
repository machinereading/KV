from collections import defaultdict
import codecs
import random
import numpy as np

class KG_dataset(object):
    
    def __init__(self, data_dir):
        ent2id = codecs.open(data_dir+"ent2id.txt", "r", encoding="utf-8")
        rel2id = codecs.open(data_dir+"rel2id.txt", "r", encoding="utf-8")
        self.word2id = dict()
        self.id2word = dict()
        wordindex = 0
        for line in ent2id.readlines():
            line = line.strip().split("\t")
            entity = line[0]
            self.word2id[entity] = wordindex
            self.id2word[wordindex] = entity
            wordindex += 1
        self.num_entities = wordindex
        for line in rel2id.readlines():
            line = line.strip().split("\t")
            relation = line[0]
            self.word2id[relation] = wordindex
            self.id2word[wordindex] = relation
            wordindex += 1
        self.num_relations = wordindex - self.num_entities
        self.num_vocab = wordindex
        
        train = codecs.open(data_dir+"train.txt", "r", encoding="utf-8")
        test = codecs.open(data_dir+"test.txt", "r", encoding="utf-8")
        self.train_triples = []
        self.test_triples = []
        for line in train.readlines():
            s, p, o = line.strip().split("\t")
            self.train_triples.append((self.word2id[s],self.word2id[p],self.word2id[o]))
        for line in test.readlines():
            s, p, o = line.strip().split("\t")
            self.test_triples.append((self.word2id[s],self.word2id[p],self.word2id[o]))
            
        self.whole_triples = self.train_triples+self.test_triples
        
        self.sbj_whole_triple_dict = defaultdict(lambda: [])
        self.obj_whole_triple_dict = defaultdict(lambda: [])
        self.sbj_train_triple_dict = defaultdict(lambda: [])
        self.obj_train_triple_dict = defaultdict(lambda: [])
        for triple in self.train_triples:
            sbj, rel, obj = triple
            self.sbj_whole_triple_dict[(sbj, rel)].append(obj)
            self.obj_whole_triple_dict[(rel, obj)].append(sbj)
            self.sbj_train_triple_dict[(sbj, rel)].append(obj)
            self.obj_train_triple_dict[(rel, obj)].append(sbj)
        for triple in self.test_triples:
            sbj, rel, obj = triple
            self.sbj_whole_triple_dict[(sbj, rel)].append(obj)
            self.obj_whole_triple_dict[(rel, obj)].append(sbj)
        
        #self.path_dict_generate()
        #self.graph_generate()
        #print("loading data done..")
    

    def path_dict_generate(self):
        self.path2id = dict()
        self.id2path = dict()
        paths = []
        #None
        paths.append(())
        for i in range(self.num_entities, self.num_vocab):
            for j in range(self.num_entities, self.num_vocab):
                paths.append((i, j))
                for k in range(self.num_entities, self.num_vocab):
                    paths.append((i,j,k))

        for i in range(len(paths)):
            #print(path)
            self.path2id[paths[i]] = i
            self.id2path[i] = paths[i]
        self.num_paths = len(paths) - len(self.path2id.keys()) + 2
    
    def graph_generate(self):
        self.graph = defaultdict(lambda: [])

        for triple in self.train_triples:
            s, p, o = triple
            self.graph[s].append((o,p))
            self.graph[o].append((s,p))
    
    def path_finding(self, start, end):
        path = []
        for first_node in self.graph[start]:
            first_ent, first_rel = first_node
            if first_ent != end:
                for second_node in self.graph[first_ent]:
                    second_ent, second_rel = second_node
                    if second_ent == end:
                        if (first_rel, second_rel) not in path:
                            path.append((first_rel, second_rel))
                    else:
                        for third_node in self.graph[second_ent]:
                            third_ent, third_rel = third_node
                            if third_ent == end:
                                if (first_rel, second_rel, third_rel) not in path:
                                    path.append((first_rel, second_rel, third_rel))
        if len(path) == 0:
            return []
        return path
    
    def path_find(self, start, end):
        for first_node in self.graph[start]:
            first_ent, _ = first_node
            if first_ent != end:
                for second_node in self.graph[first_ent]:
                    second_ent, _ = second_node
                    if second_ent == end:
                        return 1
                    else:
                        for third_node in self.graph[second_ent]:
                            third_ent, third_rel = third_node
                            if third_ent == end:
                                return 1      
        return 0
        
    def paths_to_index(self, paths):
        indices = []
        if len(paths) == 0:
            indices.append(self.path2id[()])
        else:
            for path in paths:
                indices.append(self.path2id[path])
        return indices


    def neg_sampling(self, sbj, rel, len_flag=0):
        if len_flag == 0:
            rand = np.random.randint(0, self.num_entities)
            while rand in self.sbj_whole_triple_dict[(sbj, rel)]:
                rand = np.random.randint(0, self.num_entities)
            return [sbj, rel, rand]
        elif len_flag == 1:
            related_objs = []
            for first_node in self.graph[sbj]:
                first_ent, _ = first_node
            for second_node in self.graph[first_ent]:
                second_ent, _ = second_node
                related_objs.append(second_ent)
                for third_node in self.graph[second_ent]:
                    third_ent, third_rel = third_node
                    relate_objs.append(third_ent)
            rand = random.sample(related_objs, 1)
            while rand in self.sbj_whole_triple_dict[(sbj, rel)]:
                rand = random.sample(related_objs, 1)
            return [sbj, rel, rand]
        else:
            print("Error")
            return None

    def whole_train_batch(self, len_flag=0, negative_ratio=1):
        input_x = []
        input_y = []
        
        for triple in self.train_triples:
            sbj, rel, obj = triple
            input_x.append([sbj, rel, obj])
            input_y.append((1))
        
            rand = np.random.randint(0, self.num_entities)

            # Corrupt triple by changing sbj entity
            for i in range(negative_ratio):
                neg_sample = self.neg_sampling(sbj, rel)
                input_x.append(neg_sample)
                input_y.append((0))
        
        return np.array(input_x), np.array(input_y)

    def whole_train_batch_with_path(self, len_flag, negative_ratio=1):
        input_x = []
        input_x_2 = []
        input_y = []
        
        rand_ = random.sample(self.train_triples, 10)
        
        for triple in rand_:
            sbj, rel, obj = triple
            paths = self.path_find(sbj, obj)
            input_x.append([sbj, rel, obj])
            input_x_2.append([paths])
            input_y.append((1))
            #print(triple)
        
            rand = np.random.randint(0, self.num_entities)
            # Corrupt triple by changing sbj entity
            for i in range(negative_ratio):
                neg_sample = self.neg_sampling(sbj, rel)
                paths = self.path_find(rand, obj)
                #indices = self.paths_to_index(paths)
                input_x.append([rand, rel, obj])
                input_x_2.append([paths])
                input_y.append((0))
                # Corrupt triple by changing obj entity
                rand = np.random.randint(0, self.num_entities)
        
        return np.array(input_x), np.array(input_x_2), np.array(input_y)