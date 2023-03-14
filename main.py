from managers.TrainingModel import TrainingModel
from managers.PredictionModel import PredictionModel
from managers.Functions import getNumber, getString

MODE = getNumber('Please specify what mode to run in (0 - Config Maker, 1 - Training, 2 - Predictions)')
Model = None

if MODE == 0:
    Model = TrainingModel()
    Model.runAndSetConfig()
elif MODE == 1:
    Model = TrainingModel()
    Model.runTraining()
elif MODE == 2:
    Model = PredictionModel()
    Model.setupPrediction()
    while True:
        path = getString('Please specify an image path to classify (Type \'E\' to end)')
        if path.upper() == 'E':
            break

        prediction = Model.predict(path)
        highest = prediction[0].tolist().index(max(prediction[0]))
        print(f"\nIt looks most like a {Model.labels[highest]}, I am {(prediction[0][highest] * 100)}% sure")
