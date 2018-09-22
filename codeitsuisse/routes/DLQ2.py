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

logger = logging.getLogger(__name__)


def model():
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
    model = model()
    model.load_weights("mnist-weights.yaml")
    prediction = model.predict(questions).reshape(n_samples)
    logging.info("My result :{}".format(result))
    return jsonify({"answer": prediction})
