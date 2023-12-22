#from paddleocr import PaddleOCR
import time
import re
#from api import ocr
from test import ocr
from sanct import check_sanction


import re

def extract_number(text):
    pattern = r'^[A-Za-z0-9]{7}'  # Recherche d'une séquence de 7 caractères, mélange de chiffres et de lettres au début du texte
    match = re.match(pattern, text)
    
    if match:
        return match.group(0)
    else:
        return None


def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

import re

def extract_date(text):
    pattern = r'(\d{2}[.\s-]?\d{2}[.\s-]?\d{4})'
    match = re.search(pattern, text)
    
    if match:
        date_with_possible_delimiters = match.group(1)
        date_without_delimiters = date_with_possible_delimiters.replace(".", "").replace(" ", "").replace("-", "")
        formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
        return formatted_date
    else:
        return None
    
def contains_Surname(text):
    pattern = r'(?i)Surname' 
    return re.search(pattern, text) is not None

def contains_passeport(text):
    pattern = r'(?i)PASSPORT' 
    return re.search(pattern, text) is not None
    

def contains_names(text):
    pattern = r'(?i)names' 
    return re.search(pattern, text) is not None

def contains_Given(text):
    pattern = r'(?i)Given' 
    return re.search(pattern, text) is not None
    
##NOM
    
def extract_nom_prenom(data):
    nom = ""
    prenom = ""

    for box_data in reversed(data[0]):
        text = box_data[1][0]
        if text.startswith("P<TUN"):
            parts = text.split("<<")
            #if len(parts) == 2:
            nom = parts[0][5:]  # Supprime "P<TUN" du début
            prenom = parts[1]

            nom = nom.replace("<", " ")
            prenom = prenom.replace("<", " ")
            break

    return nom, prenom

def extract_nom_prenom(data):
    nom = ""
    prenom = ""

    for box_data in reversed(data[0]):
        text = box_data[1][0]
        if text.startswith("P<TUN"):
            parts = text.split("<<")
            #if len(parts) == 2:
            nom = parts[0][5:]  # Supprime "P<TUN" du début
            prenom = parts[1]

            nom = nom.replace("<", " ")
            prenom = prenom.replace("<", " ")
            break

    return nom, prenom
## NUM ETRANGER

def process_num(data,image):
    id = ""
    for box_data in reversed(data[0]):
        text = box_data[1][0]
        if len(text) >= 7 and text[:7].isalnum():
            id = text[:7]
            break
    return id


#def process_num(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
 #   boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
  #  for box_data in reversed(data[0]):
   #     text = box_data[1][0]
    #    if extract_number(text):
     #""       boites_numeriques_trouvees = True
      #      break
    
    
   # if boites_numeriques_trouvees:
    
     #   for box_data in reversed(data[0]):

      #      if extract_number(text):
       #         box = box_data
        #        num = extract_number(box[1][0])
         #       return num

                
    #else:
     #   points = [(259, 48), (371, 48), (371, 71), (259, 71)]
      #  x, y, width, height = get_bounding_rectangle(points)
       # cropped_image = image[y:y+height, x:x+width]
        #resultat2 = ocr.ocr(cropped_image)
        #if len(resultat2[0]) > 0 :
         #   return(resultat2[0][0][1][0])
        
##############
        


## Date naissace

def process_naiss(data,image):
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
                
    else:
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
## Delai validité 

def process_validite(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if extract_date(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        count_dates = 0
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_date(text):
                count_dates+=1
                if count_dates == 4 :
                    box = data[0][i]
                    date = extract_date(box[1][0])
                    #formatted_date = date.replace(".", "/")  # Convertir . en /
                    return date
                
    else:
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])


def process_emission(data,image):
    #data = ocr.ocr(image)


    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        if extract_date(data[0][i][1][0]):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        count_dates = 0
    
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if extract_date(text):
                count_dates+=1
                if count_dates == 3 :
                    box = data[0][i]
                    date = extract_date(box[1][0])
                    #formatted_date = date.replace(".", "/")  # Convertir . en /
                    return date
                
    else:
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
## Nationalité


def process_ID(data,image):
    #data = ocr.ocr(image)


    boites_numeriques_trouvees = False
 
    for i in range(len(data[0])):
        if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) == 8:
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        
        # Extraire les boîtes ou le texte spécifique
        numeric_boxes = []
        
    
        for i in range(len(data[0])):
            if data[0][i][1][0].isdigit() and len(data[0][i][1][0]) == 8:
                numeric_boxes = [box for box in data[0][i]]
                break
        if numeric_boxes :
            return(numeric_boxes[1][0])
        #resultats_boites_numeriques.append(numeric_boxes)
    else:
        #points = [(226, 116), (377, 116), (377, 150), (226, 150)]
        points = [(216, 116), (393, 116), (393, 163), (216, 163)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])


### apply ocr

def process_image_data(image):
    data=ocr.ocr(image)
    num = process_num(data,image)
    nom , prenom = extract_nom_prenom(data)
    naissance = process_naiss(data,image)
    validité = process_validite(data,image)
    emission = process_emission(data,image)
    IdCin = process_ID(data,image)
    sanction = check_sanction(nom, prenom, naissance, "tunisienne")
    
    output = {
        "type":"PasseportTunisien",
        "nom" : nom,
        "prenom": prenom,
        "numeroEtranger": num,
        "dateNaissance":naissance,
        "dateDelivrance": emission,
        "dateValidite" : validité,
        "IdCin" : IdCin,
        "nationalite" : "tunisienne",
        "lieu" : None,
        "sanction": sanction
        
    }

    return output
import cv2
import os
def run_PassTN(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (640,640))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_recto{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_image_data(cv2.imread(cropped_recto_path))

    os.remove(cropped_recto_path)
    return output



