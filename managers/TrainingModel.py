import cv2
import os
import random
import time

import numpy as np
import tensorflow as tf
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

from managers.Functions import getJson, writeJson, getString, getNumber, doesFileExist


class TrainingModel:
    def __init__(self):
        self.config = None
        self.labels = []
        self.image_size = []
        self.data = [[], []]
        self.model = None

    def runAndSetConfig(self):
        print("   _____             __ _          _____                _             \n"
              "  / ____|           / _(_)        / ____|              | |            \n"
              " | |     ___  _ __ | |_ _  __ _  | |     _ __ ___  __ _| |_ ___  _ __ \n"
              " | |    / _ \| '_ \|  _| |/ _` | | |    | '__/ _ \/ _` | __/ _ \| '__|\n"
              " | |___| (_) | | | | | | | (_| | | |____| | |  __/ (_| | || (_) | |   \n"
              "  \_____\___/|_| |_|_| |_|\__, |  \_____|_|  \___|\__,_|\__\___/|_|   \n"
              "                           __/ |                                      \n"
              "                          |___/                                       ")
        print('Welcome to the Kipling config editor, we will now go through all the steps of creating a config\n')
        time.sleep(5)

        if not doesFileExist('./settings/config.json'):
            print('A config.json file has not been detected by our system, creating it now\n')
            writeJson('./settings/config.json', {})
            time.sleep(5)

        self.config = getJson('./settings/config.json')

        self.image_size = [
            getNumber('Please specify a width to resize images to'),
            getNumber('Please specify a height to resize images to')
        ]

        training_dir = getString('Please specify a directory for training data')
        model_dir = getString('Please specify a directory for saving the model')

        print(f"Detected the following labels from the training data ({', '.join(os.listdir('./data/training'))})")
        self.labels = os.listdir('./data/training')
        time.sleep(5)

        writeJson('./settings/config.json', {
            "directories": {
                "saved_model": model_dir,
                "training_data": training_dir
            },
            "image_size": {
                "width": self.image_size[0],
                "height": self.image_size[1]
            },
            "labels": self.labels
        })

        print('Settings have been saved to the config.json file')

    def formatData(self):
        data = []
        for label in self.labels:
            path = os.path.join(self.config['directories']['training_data'], label)
            for image in os.listdir(path):
                image_as_array = cv2.resize(cv2.imread(os.path.join(path, image)),
                                            (self.image_size[0], self.image_size[1]))
                data.append([image_as_array, self.labels.index(label)])
        random.shuffle(data)
        return data

    def setTrainingLabels(self, data):
        for features, label in data:
            self.data[0].append(features)
            self.data[1].append(label)

        self.data[0] = np.array(self.data[0]).reshape(-1, self.image_size[0], self.image_size[1], 3)
        self.data[0] = self.data[0].astype('float32')
        self.data[0] /= 255

        self.data[1] = np_utils.to_categorical(self.data[1], len(self.labels))

    def createModel(self):
        self.model = Sequential([
            Conv2D(32, (3, 3), padding='same', activation=tf.nn.leaky_relu, input_shape=(self.image_size[0], self.image_size[1], 3)),
            MaxPooling2D((2, 2), strides=2),
            Conv2D(32, (3, 3), padding='same', activation=tf.nn.leaky_relu),
            MaxPooling2D((2, 2), strides=2),
            Dropout(0.5),
            Flatten(),
            Dense(128, activation=tf.nn.leaky_relu),
            Dense(len(self.labels), activation=tf.nn.softmax)
        ])

    def runTraining(self):
        print("  _  ___       _ _                _____ _               _  __ _           \n"
              " | |/ (_)     | (_)              / ____| |             (_)/ _(_)          \n"
              " | ' / _ _ __ | |_ _ __   __ _  | |    | | __ _ ___ ___ _| |_ _  ___ _ __ \n"
              " |  < | | '_ \| | | '_ \ / _` | | |    | |/ _` / __/ __| |  _| |/ _ \ '__|\n"
              " | . \| | |_) | | | | | | (_| | | |____| | (_| \__ \__ \ | | | |  __/ |   \n"
              " |_|\_\_| .__/|_|_|_| |_|\__, |  \_____|_|\__,_|___/___/_|_| |_|\___|_|   \n"
              "        | |               __/ |                                           \n"
              "        |_|              |___/                                            "
        )
        print('Welcome to the training sector of the Kipling classifier, training will commence shortly, '
              'some background things need to be done first')

        if doesFileExist('./settings/config.json'):
            self.config = getJson('./settings/config.json')
            self.image_size = [self.config['image_size']['width'], self.config['image_size']['height']]
            self.labels = self.config['labels']

        self.setTrainingLabels(self.formatData())
        self.createModel()

        X_Train, X_Test, Y_Train, Y_Test = train_test_split(self.data[0], self.data[1], test_size=0.2, random_state=4)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(X_Train, Y_Train, batch_size=16, epochs=5, verbose=1, validation_data=(X_Test, Y_Test))

        self.model.save(self.config['directories']['saved_model'])

        print(f"\nBuilt and saved model at the path '{self.config['directories']['saved_model']}'")
        time.sleep(5)

        return self.model.evaluate(X_Test, Y_Test, verbose=0)