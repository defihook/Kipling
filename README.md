# Kipling

## Important Information
This program is built using Python `v3.11.2` and has only been tested with that, the program has been tested on both `MacOS Ventura 13.2.1` and `Windows 11`.

## Install Dependencies
* If you have `pipenv` installed 
  * Run `pipenv install`
* If not 
  * Run `pip3 install -r requirements.txt`

## Different Kipling Modes
Kipling has built in tools to help make your image classification sequence easy to build:    
  * Option 1 - The Config Creator
    * This will prompt you through some questions to create a valid `config.json` file for the network.
  * Option 2 - The Training Module
    * This will detect all labels based on your data and then train the model based on your config.
  * Option 3 - The Prediction Module
    * This will allow you to have images classified with the model.
 
 ## Config Creator
 The config creator was built to help you create a valid `config.json` file for the network, the following text will explain what each question is.
* **Width** - You must specify a width for all images to be resized to. *Type*: `Number`
* **Height** - You must specify a height for all images to be resized to. *Type*: `Number`
* **Training Data Directory** - You must specify a valid path that the model can reference for training data. *Type*: `String`
* **Saving Model Directory** - You must specify a valid path that the network can saved the trained model to. *Type*: `String`

## Training Module
The training module is completely automatic, you must let it run until the program ends, please ensure the following things before you run the training module.
* You have run the `Config Creator` and you have a valid `config.json` file.
* You have loaded in **ALL** of your training data in the following directory format.
```
<training_dir>
      |__ label_1
            |__ image1.png
            |__ image2.png
            |__ ...
            |__ image100.png
      |__ label_2
            |__ image1.png
            |__ image2.png
            |__ ...
            |__ image100.png
      |__ label_3
            |__ image1.png
            |__ image2.png
            |__ ...
            |__ image100.png
```
**You MUST** have a folder for each label you want, and in that folder you must have `.png`, `.jpg` or `.jpeg` that have that label in them. *For Example* I want to build a model that can identify a cat, a dog and a bird, view an example of how I would layout my training directory below.
```
<training_dir>
      |__ dog
            |__ dogimage1.png
            |__ dogimage2.png
            |__ ...
            |__ dogimage100.png
      |__ cat
            |__ catimage1.png
            |__ catimage2.png
            |__ ...
            |__ catimage100.png
      |__ bird
            |__ birdimage1.png
            |__ birdimage2.png
            |__ ...
            |__ birdimage3.png
```

### Note 
The more images you have of your labels, the more accurate the model will be in it's predictions.

## Prediciton Model
The prediciton model will load in your saved training model, this does mean however that you must run the training model before you can run this model. Once everything is loaded the prediction model will ask you to provide the path to an image you want classified, paste in your path and the model will predict what it is.

### Note
Not every model is perfect, you may get the wrong result, if you are continuously getting the wrong results, you may need to add more training data and then retrain your model.
