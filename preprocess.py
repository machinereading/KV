import codecs
import json
from collections import defaultdict
import os
import random

if __name__ == "__main__":
	config_json = open("run_config.json", "r")
	c = config_json.read()
	config = json.loads(c)
	config_json.close()

	training_data = config["input"]["training_data"]
	preprocess_dir = config["output"]["data_dir"]

	#os.makedirs("./"+preprocess_dir, exist_ok=True)

	data = codecs.open(training_data, "r", encoding="utf-8")
	entities = set()
	relations = set()
	triples = []

	for line in data.readlines():
		try:
			sbj, rel, obj = line.strip().split("\t")
		except:
			continue

		entities.add(sbj)
		entities.add(obj)
		relations.add(rel)
		triples.append([sbj,rel,obj])

	entities = list(entities)
	relations = list(relations)

	data.close()

	ent2id = codecs.open(preprocess_dir+"ent2id.txt", "w", encoding="utf-8")
	rel2id = codecs.open(preprocess_dir+"rel2id.txt", "w", encoding="utf-8")
	train = codecs.open(preprocess_dir+"train.txt", "w", encoding="utf-8")
	test = codecs.open(preprocess_dir+"test.txt", "w", encoding="utf-8")

	for i in range(len(entities)):
		ent2id.write(entities[i]+"\t"+str(i)+"\n")
	for i in range(len(relations)):
		rel2id.write(relations[i]+"\t"+str(i)+"\n")
	for triple in triples:
		if random.randint(0,20) == 1:
			test.write("\t".join(triple)+"\n")
		else:
			train.write("\t".join(triple)+"\n")

	print("preprocessing done.")
