from keras.models import load_model
import codecs
from KG import KG_dataset
from collections import defaultdict
import json
import gc
from scoring import normalize


def validate(kdb, validate_file, model, thresholds, output_file1, output_file2):
	f = codecs.open(validate_file, "r", encoding="utf-8")
	fw = codecs.open(output_file1, "w", encoding="utf-8")
	th_f = codecs.open(thresholds, "r", encoding="utf-8")
	fw2 = codecs.open(output_file2, "w", encoding="utf-8")

	thr_dict = dict()

	for line in th_f.readlines():
		rel, th = line.strip().split("\t")
		th = float(th)
		thr_dict[rel] = th

	model = load_model(model)
	total_triples = 0
	no_ent_or_rel = 0
	can_label = 0
	yes = 0
	no = 0
	for line in f.readlines():
		total_triples += 1
		sbj, rel, obj = [x.strip() for x in line.strip().split("\t")][:3]
		line = "\t".join([sbj, rel, obj])+ "\n"
		if sbj not in kdb.word2id.keys() or obj not in kdb.word2id.keys() or rel not in kdb.word2id.keys():
			no_ent_or_rel += 1
			fw2.write(line)
		else:
			can_label += 1

			try:
				triple = [kdb.word2id[sbj], kdb.word2id[rel], kdb.word2id[obj]]
				score = round(model.predict([[triple]])[0][0], 4)
				score = round(normalize(score), 4)

				if score >= thr_dict[rel]:
					label = 'o'
					yes += 1
				else:
					label = 'x'
					no += 1
				fw.write("\t".join([line.strip(), label, str(score)])+"\n")
			except:
				#print("entity or relation is not trained!")
				pass		
	
	print("Total triples: %d"%total_triples)
	print("Triples validated: %d"%can_label)
	print("Triples with unidentified entity or relation: %d"%no_ent_or_rel)
	print(yes, no)
	print("Done")
	fw.close()

class validator(object):
	def __init__(self, config):
		config_json = open(config, "r")
		c = config_json.read()
		self.config = json.loads(c)
		self.kdb = KG_dataset(self.config["KG"])
		self.model = load_model(self.config["model"])
		self.thr_dict = dict()
		th_f = codecs.open(self.config["thresholds"], "r", encoding="utf-8")
		for line in th_f.readlines():
			rel, th = line.strip().split("\t")
			th = float(th)
			self.thr_dict[rel] = th

	def validate(self, input_json):
		triples = input_json["PL"]["triples"]
		result_json = dict()
		result_json["PL"] = dict()
		validated_triples = []
		for triple in triples:
			sbj = triple["s"]
			rel = triple["p"]
			obj = triple["o"]

			if sbj not in self.kdb.word2id.keys() or obj not in self.kdb.word2id.keys() or rel not in self.kdb.word2id.keys():
				validated_triples.append(triple)
				print(triple)
			else:

				try:
					triple_id = [self.kdb.word2id[sbj], self.kdb.word2id[rel], self.kdb.word2id[obj]]
					score = round(self.model.predict([[triple_id]])[0][0], 4)
					score = round(normalize(score), 4)
					print(triple, score)

					if score >= self.thr_dict[rel]:
						validated_triples.append(triple)
					else:
						pass
				except:
					print("except")
					print(triple)
					validated_triples.append(triple)
		result_json["PL"]["triples"] = validated_triples

		return result_json

if __name__ == "__main__":
	config_json = open("validate_config.json", "r")
	c = config_json.read()
	config = json.loads(c)
	kdb = KG_dataset(config["input"]["KG"])
	validate(kdb, config["input"]["validate_file"], config["input"]["model"], config["input"]["thresholds"], config["output"]["classified_file"], config["output"]["no_ent_or_rel_file"])
	gc.collect()