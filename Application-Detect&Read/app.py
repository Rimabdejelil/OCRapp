import io
import base64
import subprocess
import re
import ast
from tt import run_sejourAncienVerso
import torch
#import redis
from models.experimental import attempt_load
from flask import Flask, render_template, jsonify, request
import cv2
#from detect import run_orientation
from subprocess import Popen
#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')
# -*- coding: utf-8 -*-
from flask import Flask, request , jsonify
#from paddleocr import PaddleOCR
import numpy as np
import cv2
import sys
from PIL import Image
import os
from flask import render_template,flash,redirect
from PIL import Image
import locale
import time
sys.stdout.reconfigure(encoding='utf-8')
import sys
import io
import json
import asyncio
#import tensorflow as tf
#import keras.models
from concurrent.futures import ThreadPoolExecutor
from SejourAncien import run_sejourAncien
from verso import run_verso_one , run_verso_two
from CIN_TN import run_cin
from Sejour2 import run_sejour2
from ID_FR2 import run_CINFR2
from PASSEPORT2 import run_PASSEPORT2
from Card_ID_ancien2 import run_CINFR_ancien2
from flask import Flask, request, jsonify, send_file
import subprocess
import os
#from detect_and_crop import detect
import glob
#from detect_and_crop import detect
import numpy as np
from utils.torch_utils import select_device, TracedModel
from PasseportTun import run_PassTN
from orientation import get_orientation
from sanct import check_sanction
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

sys.stdout.reconfigure(encoding='utf-8')

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

request_counter = Counter('http_requests_total', 'Total number of HTTP requests')
error_counter = Counter('http_request_errors_total', 'Total number of HTTP request errors')

# Create a histogram to measure the duration of HTTP requests
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds')



valid_key = '9e739eee1f931bd4abfb1d59ad3f9442'
def is_valid_api_key(api_key):
    return api_key == valid_key

def process_image(input_image_path, card_type, response_data):
    try:
        with app.app_context():
            request_counter.inc()

            # Record the duration of the request
            start_time = time.time()

            process = subprocess.Popen(
                ["python", "detect_and_crop1.py", "--img-size", "640", '--source', input_image_path, "--conf", "0.4",
                 "--weights", "best.pt"],
                stdout=subprocess.PIPE
            )
            process.wait()

            output = process.stdout.read().decode('utf-8')

            start_index = output.find('[[')
            end_index = output.find(']]', start_index)

            tensor_text = output[start_index:end_index + 2]
            if tensor_text:
                try:
                    tensor_data = ast.literal_eval(tensor_text)

                    pred = torch.tensor(tensor_data)

                    detected_cards = []
                    for *xyxy, conf, cls in pred:
                        if conf > 0.4:
                            xyxy_np = np.array(xyxy)
                            if (0 <= int(cls) <= 4) or (int(cls) == 8) or (int(cls) == 9):
                                detected_cards.append(
                                    {"type": "recto", "class": int(cls), "coordinates": xyxy_np.tolist()})
                            elif (5 <= int(cls) <= 7) or (5 <= int(cls) == 10):
                                detected_cards.append(
                                    {"type": "verso", "class": int(cls), "coordinates": xyxy_np.tolist()})

                    output = []
                    combined_info = {}

                    for card in detected_cards:
                        card_type = card["type"]
                        card_class = card["class"]
                        card_coordinates = card["coordinates"]

                        card_info = {}

                        if card_type == "recto":
                            if card_class == 0:
                                try:
                                    card_info.update(run_cin(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during CIN processing: {e}")
                                    return jsonify({"error": "Error during CIN processing"})
                            elif card_class == 1:
                                try:
                                    card_info.update(run_sejour2(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during Sejour processing: {e}")
                                    return jsonify({"error": "Error during Sejour processing"})
                            elif card_class == 2:
                                try:
                                    card_info.update(run_PASSEPORT2(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during PASSEPORT processing: {e}")
                                    return jsonify({"error": "Error during PASSEPORT processing"})
                            elif card_class == 3:
                                try:
                                    card_info.update(run_CINFR_ancien2(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during CINFRANCIEN processing: {e}")
                                    return jsonify({"error": "Error during CINFRANCIEN processing"})
                            elif card_class == 4:
                                try:
                                    card_info.update(run_CINFR2(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during CINFR processing: {e}")
                                    return jsonify({"error": "Error during CINFR processing"})
                            elif card_class == 8:
                                try:
                                    card_info.update(run_PassTN(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during PasseportTN processing: {e}")
                                    return jsonify({"error": "Error during PasseportTN processing"})
                            elif card_class == 9:
                                try:
                                    card_info.update(run_sejourAncien(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during SejourAncien processing: {e}")
                                    return jsonify({"error": "Error during SejourAncien processing"})

                        elif card_type == "verso":
                            if card_class == 5:
                                try:
                                    card_info.update(run_verso_two(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during CINFRANCIENVERSO processing: {e}")
                                    return jsonify({"error": "Error during CINFRANCIENVERSO processing"})
                            elif card_class == 6:
                                try:
                                    card_info.update(run_verso_one(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during TitreSejourFRVerso processing: {e}")
                                    return jsonify({"error": "Error during TitreSejourFRVerso processing"})
                            elif card_class == 7:
                                try:
                                    card_info.update(run_verso_one(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during CINFRVerso processing: {e}")
                                    return jsonify({"error": "Error during CINFRVerso processing"})

                            elif card_class == 10:
                                try:
                                    card_info.update(run_sejourAncienVerso(input_image_path, card_coordinates))
                                except Exception as e:
                                    print(f"An error occurred during SejourFrAncienVerso processing: {e}")
                                    return jsonify({"error": "Error during SejourFrAncienVerso processing"})
                        combined_info.update(card_info)
                    output.append(combined_info)
                    # os.remove(input_image_path)
                    response_data.update(combined_info)
                    request_duration.observe(time.time() - start_time)

                    return response_data,card_class
                except Exception as e:
                    print(f"An error in the image format: {e}")
                    return jsonify({"error": "Error in the image format"})

            else:
                os.remove(input_image_path)
                return jsonify({"error": "Error in the image format"})

    except Exception as e:
        print(f"An error occurred during image processing: {e}")
        return jsonify({"error": "Error during image processing"})

    

from flask import render_template

@app.route('/kyc')
def index():
    return render_template('index.html')

@app.route('/kyc_v2', methods=['POST'])
def kyc():

    if 'recto_image' not in request.files and 'verso_image' not in request.files :
        return jsonify({"error": "Both recto_image and verso_image are missing."})

    


        
        
    elif 'recto_image' in request.files and 'verso_image' not in request.files  :
        recto_image = request.files['recto_image']
        
        if (recto_image.filename) :
            try:
        #recto_image = request.files['recto_image']
                recto = f"static/recto.jpg" 
                recto_image.save(recto)

                o = get_orientation(recto)
                if o == 3 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 1))
                    os.remove(recto)
                    recto = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                elif o == 2 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 2))
                    os.remove(recto)
                    recto = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                elif o == 1:
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 3))
                    os.remove(recto)
                    recto = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                response_data = {}
        

                with ThreadPoolExecutor(max_workers=2) as executor:
                    recto_future = executor.submit(process_image, recto, "recto", response_data)

                    recto_results , card_class = recto_future.result()
                    if card_class == 3:
                        recto_results["dateValidite"] = None
                        recto_results["dateDelivrance"] = None

                    elif card_class == 9:
                        recto_results["nom"] = None
                        recto_results["prenom"] = None
                        recto_results["sanction"]=None


            
                    response_data.update(recto_results)
            except Exception as e :
                response_data = {'error': 'Invalid data', 'message': str(e)}
    elif 'recto_image' in request.files and 'verso_image' in request.files  :
        recto_image = request.files['recto_image']
        verso_image = request.files['verso_image']

        if not (recto_image.filename) and not (verso_image.filename) :
            return jsonify({"error": "no images selected"})
        
        if ((recto_image.filename) and (not verso_image.filename)):
            try:
                recto = f"static/recto.jpg"  
                recto_image.save(recto)
                o = get_orientation(recto)
                if o == 3 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 1))
                    os.remove(recto)
                    recto = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                elif o == 2 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 2))
                    os.remove(recto)
                    recto = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                elif o == 1:
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 3))
                    os.remove(recto)
                    recto = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                response_data = {}
        

                with ThreadPoolExecutor(max_workers=2) as executor:
                    recto_future = executor.submit(process_image, recto, "recto", response_data)

                    recto_results , card_class = recto_future.result()
                    if card_class == 3:
                        recto_results["dateValidite"] = None
                        recto_results["dateDelivrance"] = None

                    elif card_class == 9:
                        recto_results["nom"] = None
                        recto_results["prenom"] = None
                        recto_results["sanction"] = None


            
                    response_data.update(recto_results)
            except Exception as e :
                response_data = {'error': 'Invalid data', 'message': str(e)}
    
        elif not recto_image.filename and verso_image.filename :

            try : 

                verso = f"verso_{int(time.time())}.jpg" 
                verso_image.save(verso)
                o = get_orientation(verso)
                if o == 3 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(verso), 1))
                    os.remove(verso)
                    verso = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(verso, detected_orientation)
                elif o == 2 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(verso), 2))
                    os.remove(verso)
                    verso = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(verso, detected_orientation)
                elif o == 1:
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(verso), 3))
                    os.remove(verso)
                    verso = f"orient_{int(time.time())}.jpg"
                    cv2.imwrite(verso, detected_orientation)
                response_data = {}

                with ThreadPoolExecutor(max_workers=2) as executor:
                    verso_future = executor.submit(process_image, verso, "verso", response_data)

                    verso_results , card_class= verso_future.result()

                    if card_class == 3:
                        verso_results["dateValidite"] = None
                        verso_results["dateDelivrance"] = None

                    elif card_class == 9:
                        verso_results["nom"] = None
                        verso_results["prenom"] = None
                        verso_results["sanction"] = None
            
                    response_data.update(verso_results)
        
            except Exception as e :
                response_data = {'error': 'Invalid data', 'message': str(e)}

        else:   
            response_data = {}
            try:

                recto = f"recto_{int(time.time())}.jpg"  
                recto_image.save(recto)
                verso = f"verso_{int(time.time())}.jpg"  
                verso_image.save(verso)

                o = get_orientation(recto)
                if o == 3 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 1))
                    os.remove(recto)
                    recto = f"orient_recto{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                elif o == 2 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 2))
                    os.remove(recto)
                    recto = f"orient_recto{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
                elif o == 1:
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(recto), 3))
                    os.remove(recto)
                    recto = f"orient_recto{int(time.time())}.jpg"
                    cv2.imwrite(recto, detected_orientation)
            
                w = get_orientation(verso)
                if w == 3 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(verso), 1))
                    os.remove(verso)
                    verso = f"orient_verso{int(time.time())}.jpg"
                    cv2.imwrite(verso, detected_orientation)
                elif w == 2 :
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(verso), 2))
                    os.remove(verso)
                    verso = f"orient_verso{int(time.time())}.jpg"
                    cv2.imwrite(verso, detected_orientation)
                elif w == 1:
                    detected_orientation = np.ascontiguousarray(np.rot90(cv2.imread(verso), 3))
                    os.remove(verso)
                    verso = f"orient_verso{int(time.time())}.jpg"
                    cv2.imwrite(verso, detected_orientation)



                with ThreadPoolExecutor(max_workers=2) as executor:
                    verso_future = executor.submit(process_image, verso, "verso",response_data)
                    recto_future = executor.submit(process_image, recto, "recto",response_data)

                if not isinstance(verso_future.result(), tuple) and isinstance(recto_future.result(), tuple) :
                    recto_results , card_recto_class = recto_future.result()
                    if card_recto_class == 3:
                        recto_results["dateValidite"] = None
                        recto_results["dateDelivrance"] = None

                    elif card_recto_class == 9:
                        recto_results["nom"] = None
                        recto_results["prenom"] = None
                        recto_results["sanction"] = None
                    
                    response_data.update(recto_results)
                    

                elif not isinstance(recto_future.result(), tuple) and isinstance(verso_future.result(), tuple) : 
                    verso_results , card_verso_class = verso_future.result()
                    if card_verso_class == 3:
                        verso_results["dateValidite"] = None
                        verso_results["dateDelivrance"] = None

                    elif card_verso_class == 9:
                        verso_results["nom"] = None
                        verso_results["prenom"] = None
                        verso_results["sanction"] = None
                    
                    response_data.update(verso_results)

                else :

                    recto_results , card_recto_class = recto_future.result()
                    verso_results , card_verso_class = verso_future.result()


                    if card_recto_class == 9  :
                        recto_results["sanction"] = check_sanction(verso_results["nom"], verso_results["prenom"], recto_results["dateNaissance"], "tunisienne")
            
                    
                    response_data.update(recto_results)
                    response_data.update(verso_results)
                    



                
            except Exception as e:
                response_data = {'error': 'Invalid data', 'message': str(e)}
                



    if "error" not in response_data :
        response_data["image_path"] = recto
        response_data["status"] = 200
        return render_template('index.html', response_data=response_data)
    else :
        response_data["status"] = 203
        return render_template('index.html', response_data=response_data)
        

# Route for Prometheus metrics
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
