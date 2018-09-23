import logging

from flask import request, jsonify
import numpy as np
import keras
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.models import Sequential
from keras.utils import np_utils
import numpy as np
from codeitsuisse import app
import os

logger = logging.getLogger(__name__)


def modelA():
    model = Sequential()
    model.add(Convolution2D(
        32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(Convolution2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    return model


@app.route('/machine-learning/question-2', methods=['POST'])
def evaluate_mlq2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    n_samples = np.array(data["question"]).shape[0]
    questions = np.array(data["question"]).reshape((n_samples, 28, 28, 1))
    model = modelA()
    model.load_weights(os.path.dirname(os.path.abspath(__file__))+"/"+"mnist-weights.yaml")
    prediction = model.predict(questions).reshape(n_samples, 10)
    output = []
    for i in prediction:
        output.append(np.argmax(i))
    return jsonify({"answer": output})
