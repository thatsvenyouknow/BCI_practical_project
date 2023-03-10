from natsort import natsorted
import numpy as np
import os
import random

def make_dataset(dict_path, val_size = 0.2):
    '''
    dict_path: path with preprocessed npy files
    val_size: rel. size of validations set
    '''
    if not os.path.exists("train_visual"):
        os.mkdir("train_visual")
        os.mkdir("val_visual")
        os.mkdir("train_multi")
        os.mkdir("val_multi")
    
    experiments = {
        "visual": ["sub1_", "sub2", "sub3", "sub4", "sub5", "sub6", "sub7", "sub8"],
        "multi": ["sub9", "sub10", "sub11", "sub12", "sub13", "sub14", "sub15", "sub16"]
    }
    
    id, t_count, v_count = 0, 0, 0
    for experiment in experiments.keys():
        train_labels, val_labels = [], []
        for sub in experiments[experiment]:
            id+=1
            for path in natsorted(os.listdir("C:/Users/Daydreamore/Desktop/Semester/BCI")):
                if path.startswith(sub) & path.endswith("preprocessed.npy"):
                    sub_data = np.load(path, allow_pickle=True).item()
                    for ix, condition in enumerate(sub_data.keys()):
                        random.shuffle(sub_data[condition])
                        split_ix = int(len(sub_data[condition])*val_size)
                        train_set = sub_data[condition][split_ix:]
                        val_set = sub_data[condition][:split_ix]
                        train_labels.append([ix]*len(train_set))
                        val_labels.append([ix]*len(val_set))
                        
                        for sample in train_set:
                            np.save("train_{}/{}_sub{}_class{}.npy".format(experiment, t_count, id, ix), sample[:,:165])
                            t_count += 1

                        for sample in val_set:
                            np.save("val_{}/{}_sub{}_class{}.npy".format(experiment, v_count, id, ix), sample[:,:165])
                            v_count += 1
                                
        np.save("train_{}/labels.npy".format(experiment), np.hstack(np.array(train_labels)))
        np.save("val_{}/labels.npy".format(experiment), np.hstack(np.array(val_labels)))

#Create dataset
make_dataset("C:/Users/Daydreamore/Desktop/Semester/BCI")