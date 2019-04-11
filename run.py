import os
import json

config_json = open("run_config.json")
c = config_json.read()
config = json.loads(c)

training_data = config["input"]["training_data"]
data_dir = config["output"]["data_dir"]
model_name = config["input"]["model"]
model_output = config["output"]["model_output"]
threshold_dir = config["output"]["thresholds_output"]



# 1.Preprocessing: Tab-delimited triples -> ent2id, rel2id, train
print('[1. Preprocessing] Creating dataset files for training ...')
print(' --- preprocessing ' + training_data + ' ...')
os.system('python3 preprocess.py')
print(' --- Data preprocessed in ' + data_dir)


# 2. Training: Training KBC model based on the input triples
print('[2. Training] Training model based on ' + training_data + ' ...')
print(' --- training ' + model_name + ' model ...')
os.system('python3 train.py')
print(' --- Done')
print(' --- model saved in ' + model_output)


# 3. Calculating Thresholds: Calculating thresholds for each relation
print('[3. Calculating Thresholds] Calculating thresholds for each relation of model ' + model_name + '...')
print(' --- calculating ... ')
os.system('python3 threshold.py')
print(' --- Done')
print(' --- thresholds saved in ' + threshold_dir)