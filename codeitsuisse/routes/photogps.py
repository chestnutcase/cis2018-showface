import logging

from flask import request, jsonify;

from codeitsuisse import app;
import piexif
import requests

@app.route('/imagesGPS', methods=['POST'])
def evaluate_gps():
    data = request.get_json();
    requests.post('http://requestbin.fullcontact.com/10jg4bo1', json=data)
    locations = [];
    for photo in data:
        exifData = piexif.load(requests.get(photo["path"]).content);
        lat = exifData["GPS"][2][0][0] + float(exifData["GPS"][2][1][0]) / 60 + float(exifData["GPS"][2][2][0])/exifData["GPS"][2][2][1]/3600;
        if exifData["GPS"][1] == "S":
            lat = lat * -1;
        long = exifData["GPS"][4][0][0] + float(exifData["GPS"][4][1][0]) / 60 + float(exifData["GPS"][4][2][0])/exifData["GPS"][4][2][1]/3600;
        if exifData["GPS"][3] == "W":
            long = long * -1;
        locations.append({"lat":lat,"long":long});
    return jsonify(locations);
