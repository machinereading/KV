from keras.layers import Embedding, Dense, Dropout, Activation, Flatten, Conv2D, pooling, Reshape, Permute
from keras.utils import np_utils
from keras.initializers import TruncatedNormal
from keras.losses import binary_crossentropy
from keras.optimizers import Adam
from keras.models import Sequential
import json

def ConvKB(kg, param):
	num_entities = kg.num_entities
	num_relations = kg.num_relations

	emb_dim = param["embedding_dimensions"]
	num_filters = param["number_of_filters"]
	dropout = param["dropout"]
	learning_rate =  param["learning_rate"]

	model = Sequential()
	model.add(Embedding(num_entities+num_relations, emb_dim, embeddings_initializer=TruncatedNormal(mean=0.0, stddev=0.1), input_length=3))
	model.add(Permute((2,1)))
	model.add(Reshape((1, emb_dim, 3)))
	model.add(Conv2D(num_filters, [1,3], strides=(1,1), padding='same', activation='relu'))
	model.add(Dropout(dropout))
	model.add(Flatten())
	model.add(Dense(1, kernel_initializer=TruncatedNormal(mean=0.0, stddev=0.05)))

	model.compile(optimizer=Adam(lr=learning_rate), loss='binary_crossentropy', metrics=['accuracy'])

	return model

def KBCNN(kg, param):
	num_entities = kg.num_entities
	num_relations = kg.num_relations

	emb_dim = param["embedding_dimensions"]
	num_filters = param["number_of_filters"]
	dropout = param["dropout"]
	learning_rate =  param["learning_rate"]

	model = Sequential()
	model.add(Embedding(num_entities+num_relations, emb_dim, embeddings_initializer=TruncatedNormal(mean=0.0, stddev=0.1), input_length=3))
	model.add(Permute((2,1)))
	model.add(Reshape((1, emb_dim, 3)))
	model.add(Conv2D(num_filters, [3,3], strides=(1,1), padding='same', activation='relu'))
	model.add(Dropout(dropout))
	model.add(Flatten())
	model.add(Dense(1, kernel_initializer=TruncatedNormal(mean=0.0, stddev=0.05)))

	model.compile(optimizer=Adam(lr=learning_rate), loss='binary_crossentropy', metrics=['accuracy'])

	return model

def KBCNN_path(kg, param):
	num_entities = kg.num_entities
	num_relations = kg.num_relations
	num_paths = kg.num_paths

	emb_dim = param["embedding_dimensions"]
	num_filters = param["number_of_filters"]
	dropout = param["dropout"]
	learning_rate =  param["learning_rate"]

	model1 = Sequential(layers=[
    Embedding(num_entities+num_relations, emb_dim, embeddings_initializer=TruncatedNormal(mean=0.0, stddev=0.1), input_length=3),
    Permute((2,1)),
    Reshape((1, emb_dim, 3)),
    Conv2D(num_filters, [3,3], strides=(1,1), padding='same', activation='relu'),
	])

	model2 = Sequential()
	model2.add(Embedding(num_paths, emb_dim, embeddings_initializer=TruncatedNormal(mean=0.0, stddev=0.1)))
	model2.add(Lambda(lambda x: K.mean(x, axis=0)))
	model2.add(Reshape((1, emb_dim,)))
	model2.add(Lambda(lambda x: K.expand_dims(x)))

	mergedOut = Concatenate()([model1.output, model2.output])
	mergedOut = Flatten()(mergedOut)
	mergedOut = Dropout(0.3)(mergedOut)
	mergedOut = Dense(1, kernel_initializer=TruncatedNormal(mean=0.0, stddev=0.05))(mergedOut)

	pathmodel = Model([model1.input, model2.input], mergedOut)

	pathmodel.compile(optimizer=Adam(lr=0.0005), loss='binary_crossentropy', metrics=['accuracy'])

	return model

def model_wrapper(kg, param, model):
	if 'ConvKB' in model:
		return ConvKB(kg, param)
	elif 'KBCNN' in model:
		return KBCNN(kg, param)
	else:
		return KBCNN_path(kg, param)