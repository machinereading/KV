from scoring import triples_score_calculate
from scoring import score_calculate_one
from KG import KG_dataset
import json
import codecs
from collections import defaultdict
from sklearn.metrics import precision_recall_curve, average_precision_score
import numpy as np
import random
from keras.models import load_model
import os

def threshold_by_test_data(kdb, cofig):
	train = codecs.open(config["output"]["data_dir"]+"train.txt", "r", encoding="utf-8")
	test = codecs.open(config["output"]["data_dir"]+"test.txt", "r", encoding="utf-8")

	f = codecs.open(config["output"]["test_scores"], "w", encoding="utf-8")
	fw = codecs.open(config["output"]["thresholds_output"], "w", encoding="utf-8")

	whole_triple_dict = defaultdict(lambda: [])
	test_triple_dict = defaultdict(lambda: [])
	test_dict = defaultdict(lambda:[])

	for line in train.readlines():
		sbj, rel, obj = [kdb.word2id[x] for x in line.strip().split("\t")]
		whole_triple_dict[(sbj, rel)].append(obj)
	for line in test.readlines():
		sbj, rel, obj = [kdb.word2id[x] for x in line.strip().split("\t")]
		whole_triple_dict[(sbj, rel)].append(obj)
		test_triple_dict[(sbj, rel)].append(obj)
		test_dict[rel].append((sbj, rel, obj))

	triples = []
	labels = []
	triple_label_score_by_rel = dict()
	threshold_dict = dict()

	model = load_model(config["output"]["model_output"])

	for rel in test_dict.keys():
		try:
			triples = random.sample([list(x) for x in test_dict[rel]], 100)
		except:
			triples = [list(x) for x in test_dict[rel]]
		labels = [1] * len(triples)
		for i in range(len(triples)):
			sbj = triples[i][0]
			for j in range(4):
				neg_is_true = 1
				while neg_is_true:
					obj = random.randint(0, kdb.num_entities)
					if obj in whole_triple_dict[(sbj, rel)]:
						neg_is_true = 1
					else:
						neg_is_true = 0
				triple = [sbj, rel, obj]
				triples.append(triple)
				labels.append(0)

		triple_label_score = triples_score_calculate(kdb, model, triples, labels)
		triple_label_score_by_rel[rel] = list(triple_label_score)

		#print(triple_label_score)

		rel_labels = []
		rel_scores = []
		for tls in triple_label_score:
			rel_labels.append(int(tls[3]))
			rel_scores.append(float(tls[4]))
		p, r, threshold = precision_recall_curve(rel_labels, rel_scores)
		precision = p[:-1]
		recall = r[:-1]
		best_f1 = 0
		best_threshold = 0
		for i in range(len(threshold)):
			pc = precision[i]
			re = recall[i]
			try:
				f1 = pc*re / (pc+re)
			except:
				pass
			if f1 > best_f1:
				best_f1 = f1
				best_threshold = threshold[i]
		best_threshold = (best_threshold-0.5)*0.07 + 0.5
		threshold_dict[rel] = "%0.4f"%best_threshold
		#print(kdb.id2word[rel], threshold_dict[rel])

	for rel in triple_label_score_by_rel.keys():
		for tls in triple_label_score_by_rel[rel]:
			f.write("\t".join(tls)+"\n")

	for rel in threshold_dict.keys():
		fw.write(kdb.id2word[rel]+"\t"+threshold_dict[rel]+"\n")

	#score_calculate_one(kdb, config["input"]["labeled_file"], config["input"]["model"], config["output"]["triple_scores"])

if __name__ == "__main__":
	config_json = open("run_config.json", "r")
	print(config_json)
	c = config_json.read()
	config = json.loads(c)
	data_dir = config["output"]["data_dir"]
	kdb = KG_dataset(data_dir)
	threshold_by_test_data(kdb, config)


