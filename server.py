import os
import json

import tensorflow as tf
import numpy as np
from PIL import Image

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename

incep_res_model = tf.keras.applications.inception_v3.InceptionV3()
incep_res_model._make_predict_function()

recyclable = json.load(open('/root/feedme/recyclable.json'))

app = Flask(__name__)
app.secret_key = b'feedme'
socketio = SocketIO(app)

def save_post_img(img):
    # print(type(img))
    img_path = 'uploads/' + secure_filename(img.filename)
    img.save(img_path)
    return img_path

@app.route('/predict', methods=['POST'])
def incep_res_predict():
    img_path = save_post_img(request.files['image'])
    im = tf.keras.preprocessing.image.load_img(img_path, target_size=(299, 299))
    im_array = tf.keras.preprocessing.image.img_to_array(im)
    im_batch = np.expand_dims(im_array, axis=0)
    processed = tf.keras.applications.inception_v3.preprocess_input(im_batch.copy())
    predictions = incep_res_model.predict(processed)
    decoded = tf.keras.applications.inception_v3.decode_predictions(predictions)

    result = {label: float(confidence) for _, label, confidence in decoded[0]}
    data = sorted(result.keys(), key=lambda x: result[x])[-1]
    final = [data, recyclable[data]]

    socketio.emit('new', final, json=True)
    return jsonify(final)

@socketio.on('connect')
def new_connection():
    # Return all saved data
    pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
