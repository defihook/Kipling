import numpy as np

import keras
from keras.utils import image_utils

from managers.Functions import getJson, doesFileExist


class PredictionModel:
    def __init__(self):
        self.config = None
        self.labels = []
        self.image_size = []
        self.model = None

    def setupPrediction(self):
        print("  _  ___       _ _                _____ _               _  __ _           \n"
              " | |/ (_)     | (_)              / ____| |             (_)/ _(_)          \n"
              " | ' / _ _ __ | |_ _ __   __ _  | |    | | __ _ ___ ___ _| |_ _  ___ _ __ \n"
              " |  < | | '_ \| | | '_ \ / _` | | |    | |/ _` / __/ __| |  _| |/ _ \ '__|\n"
              " | . \| | |_) | | | | | | (_| | | |____| | (_| \__ \__ \ | | | |  __/ |   \n"
              " |_|\_\_| .__/|_|_|_| |_|\__, |  \_____|_|\__,_|___/___/_|_| |_|\___|_|   \n"
              "        | |               __/ |                                           \n"
              "        |_|              |___/                                            "
        )
        print('Welcome to the prediction sector of the Kipling classifier, before I can predict a few things need to '
              'be setup in the background')

        if doesFileExist('./settings/config.json'):
            self.config = getJson('./settings/config.json')
            self.image_size = [self.config['image_size']['width'], self.config['image_size']['height']]
            self.labels = self.config['labels']
        else:
            print('Please run config creator to create a config file')
            exit(0)

        self.model = keras.models.load_model(self.config['directories']['saved_model'])

        print('Loaded in Kipling Model successfully. . .')

    def predict(self, path):
        image = image_utils.load_img(path, target_size=(self.image_size[0], self.image_size[1]))
        image_array = image_utils.img_to_array(image)
        image_batch = np.expand_dims(image_array, axis=0)
        return self.model.predict(image_batch)