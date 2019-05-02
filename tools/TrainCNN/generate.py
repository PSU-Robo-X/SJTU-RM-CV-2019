import numpy as np
import os
import cv2
import random
from forward import OUTPUT_NODES
import sys
import os
from tqdm import tqdm
# 原图像行数
SRC_ROWS = 36

# 原图像列数
SRC_COLS = 48

# 原图像通道数
SRC_CHANNELS = 3


class DataSet:
    def __init__(self, folder):
        self.train_samples = []
        self.train_labels = []
        self.test_samples = []
        self.test_labels = []
        self.generate_data_sets(folder)

    def generate_data_sets(self, folder):
        def id2label(id):
            a = np.zeros([OUTPUT_NODES])
            a[id] = 1
            return a[:]

        def file2nparray(name):
            try:
                image = cv2.imread(name)
                if image.shape[0] < 15:
                    return None
                elif image.shape[1] < 10:
                    return None
                image = cv2.resize(image, (SRC_COLS, SRC_ROWS))
                image = image.astype(np.float32)
                return image / 255.0, id2label(int(name.split("/")[-2]))
            except TypeError:
                print(name)
                sys.exit(-1)

        sets = []
        for i in range(OUTPUT_NODES):
            dir = "%s/%d" % (folder, i)
            files = os.listdir(dir)
            for file in tqdm(files, postfix={"loading id": i}, dynamic_ncols=True):
                if file[-3:] == "jpg":
                    x = file2nparray("%s/%s" % (dir, file))
                    if x is not None:
                        if random.random() > 0.2:
                            self.train_samples.append(x[0])
                            self.train_labels.append(x[1])
                        else:
                            self.test_samples.append(x[0])
                            self.test_labels.append(x[1])
        self.train_samples = np.array(self.train_samples)
        self.train_labels = np.array(self.train_labels)
        self.test_samples = np.array(self.test_samples)
        self.test_labels = np.array(self.test_labels)
        return sets

    def sample_train_sets(self, length):
        samples = []
        labels = []
        for i in range(length):
            id = random.randint(0, len(self.train_samples)-1)
            samples.append(self.train_samples[id])
            labels.append(self.train_labels[id])
        return np.array(samples), np.array(labels)

    def sample_test_sets(self, length):
        samples = []
        labels = []
        for i in range(length):
            id = random.randint(0, len(self.test_samples)-1)
            samples.append(self.test_samples[id])
            labels.append(self.test_labels[id])
        return np.array(samples), np.array(labels)

    def all_train_sets(self):
        return self.train_samples[:], self.train_labels[:]

    def all_test_sets(self):
        return self.test_samples[:], self.test_labels[:]
