from keras.models import load_model
import codecs

# normalization max/min scores
NORM_MAX = 10
NORM_MIN = -10

def normalize(score):
	normalized_score = (score-NORM_MIN) / (NORM_MAX - NORM_MIN)
	if normalized_score < 0:
		normalized_score = 0
	if normalized_score > 1:
		normalized_score = 1
	return normalized_score

def score_calculate(kdb, validation_file, model_files, score_file):

	f = codecs.open(validation_file, "r", encoding="utf-8")
	fw = codecs.open(score_file, "w", encoding="utf-8")
	
	models = []

	for filename in model_files:
		models.append(load_model(filename))

	for line in f.readlines():
		sbj, rel, obj, label = line.strip().split("\t")
		triple = [kdb.word2id[sbj], kdb.word2id[rel], kdb.word2id[obj]]
		scores = []
		for model in models:
			score = round(model.predict([[triple]])[0][0], 4)
			score = round(normalize(score), 4)
			scores.append(str(score))
		fw.write("\t".join([sbj, rel, obj, label]+scores)+"\n")
	fw.close()

def score_calculate_one(kdb, validation_file, model, score_file):

	f = codecs.open(validation_file, "r", encoding="utf-8")
	fw = codecs.open(score_file, "w", encoding="utf-8")
	model = load_model(model)
	for line in f.readlines():
		sbj, rel, obj, label = line.strip().split("\t")
		triple = [kdb.word2id[sbj], kdb.word2id[rel], kdb.word2id[obj]]
		score = round(model.predict([[triple]])[0][0], 4)
		score = round(normalize(score), 4)
		score = normalize(score)
		score = str(score)
		fw.write("\t".join([sbj, rel, obj, label, score])+"\n")
	fw.close()

def triples_score_calculate(kdb, loaded_model, triples, labels):
	triple_label_score = []

	for i in range(len(triples)):
		triple = triples[i]
		label = labels[i]
		score = round(loaded_model.predict([[triple]])[0][0], 4)
		score = str(normalize(score))
		triple = [kdb.id2word[x] for x in triple]
		triple_label_score.append(triple+[str(label), score])
	return triple_label_score
	


def triple_score_caculate(kdb, triple, model_file):
	model = load_model(model_file)

	# Triple must be in utf-8
	# a list of [sbj, rel, obj]
	sbj, rel, obj = triple
	triple_in_id = [kdb.word2id[sbj], kdb.word2id[rel], kdb.word2id[obj]]

	return round(model.predict([[triple_in_id]])[0][0], 4)