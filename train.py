from KG import KG_dataset
from model import model_wrapper
import numpy as np
import json
import sys

def train_and_save_model(model, kg, param, model_name, path_flag=0):
    #epochs_per_fit = len(fb15k.train_triples) // batch_size
    epochs = param["epochs"]
    batch_size = param["batch_size"]
    negative_sample_ratio = param["negative_sample_ratio"]

    for i in range(epochs):
        print("%d th epoch" % i)

        if path_flag == 0:
            train_x, train_y = kg.whole_train_batch(negative_ratio=negative_sample_ratio)
            model.fit(train_x, train_y, batch_size=batch_size, epochs=1, verbose=1)
        elif path_flag == 1:
            train_x, train_x_2, train_y = kg.whole_train_batch_with_path(negative_ratio=negative_sample_ratio)
            model.fit([train_x, train_x_2], train_y, batch_size=batch_size, epochs=1, verbose=1)

        model.save(model_name)

    return model

def main():
    config_json = open("run_config.json", "r")
    c = config_json.read()
    config = json.loads(c)

    dataset = config["output"]["data_dir"]

    kg = KG_dataset(dataset)
    which_model = config["input"]["model"]
    param = config["input"]["hyperparam"]
    compiled_model = model_wrapper(kg, param, which_model)

    model_name = config["output"]["model_output"]
    train_and_save_model(compiled_model, kg, param, model_name)



if __name__ =="__main__":
    main()

    