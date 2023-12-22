import re
import time
from test import ocr
#from paddleocr import PaddleOCR
#ocr = PaddleOCR(use_angle_cls=True,lang='fr')

def extract_date(text):
    pattern = r'(\d{2}[.\s/-]?\d{2}[.\s/-]?\d{4})'
    matches = re.findall(pattern, text)
    
    for match in matches:
        # Remove any non-numeric characters from the matched date
        date_without_delimiters = re.sub(r'[^\d]', '', match)
        
        # Check if the cleaned date has the correct format
        if (len(date_without_delimiters) == 8) :
            formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
            return(formatted_date)
         
    
    # If no valid date is found, return None
    return None
    
def process_naiss(data):
    #data = ocr.ocr(image)

    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if extract_date(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_date(text):
                box = data[0][i]
                date = extract_date(box[1][0])
                #formatted_date = date.replace(".", "/")  # Convertir . en /
                return date
            
def extract_nom_prenom(data):
    nom = ""
    prenom = ""

    for box_data in reversed(data[0]):
        text = box_data[1][0]
        if text.endswith("<<<<<"):
            parts = text.split("<<")
            #if len(parts) == 2:
            nom = parts[0]  # Supprime "P<TUN" du début
            prenom = parts[1]

            nom = nom.replace("<", " ")
            prenom = prenom.replace("<", " ")
            break

    return nom, prenom


def process_image_data(image):
    data=ocr.ocr(image)
    
    #print(data)
    #num = process_num(data,image)
    #nom = process_nom(data,image) 
    #prenom = process_prenom(data,image)
    nom , prenom = extract_nom_prenom(data)
    #naissance = process_naiss(data)
    output = {
        "type":"titreSejourFRancien",
        "nom" : nom,
        "prenom": prenom,
        #"numeroEtranger": num,
        #"dateNaissance":naissance,
        #"dateDelivrance": delivrance,
        #"dateValidite" : validité,
        #"nationalite" : natio,
        #"lieu" : None,
        #"IdCin" : None,
    }

    return output

import cv2
import os
def run_sejourAncienVerso(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (697,433))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_verso_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))

    os.remove(cropped_recto_path)
    return output
