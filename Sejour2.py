#from paddleocr import PaddleOCR
import time
import re
#from api import ocr
from test import ocr
from sanct import check_sanction


def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

def extract_date(text):
    pattern = r'(\d{2}[.\s]?\d{2}[.\s]?\d{4})'
    match = re.search(pattern, text)
    
    if match:
        date_with_possible_delimiters = match.group(1)
        date_without_delimiters = date_with_possible_delimiters.replace(".", "").replace(" ", "")
        formatted_date = f"{date_without_delimiters[:2]}/{date_without_delimiters[2:4]}/{date_without_delimiters[4:]}"
        return formatted_date
    else:
        return None
    

def contains_sex(text):
    return "SEX" in text

def remove_asterisk(word):
    if word.endswith("*"):
        return word[:-1]  # Remove the last character (the asterisk)
    else:
        return word
    
##NOM
    
def process_nom(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if contains_sex(data[0][i][1][0]):
            boites = True
            break
            
    if boites :
        for i in range (len(data[0])):
            if contains_sex(data[0][i][1][0]):
                box = data[0][i-2]
                nom = remove_asterisk(box[1][0])
                return(nom)
               
    else :
        points =[(273, 111), (375, 111), (377, 144), (275, 145)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(remove_asterisk(resultat2[0][0][1][0]))
        
##PRENOM

def process_prenom(data,image):
    #data=ocr.ocr(image)
    
    boites = False
    
    for i in range (len(data[0])):
        if contains_sex(data[0][i][1][0]):
            boites = True
            break
            
    if boites :
        for i in range (len(data[0])):
            if contains_sex(data[0][i][1][0]):
                box = data[0][i-1]
                nom = remove_asterisk(box[1][0])
                return(nom)
    else :
        points =[(271, 142), (373, 142), (375, 175), (273, 176)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])

## NUM ETRANGER

def process_num(data,image):
    #data = ocr.ocr(image)

    # Parcourir l'output
    boites_numeriques_trouvees = False
    
    # Parcourir les éléments dans chaque élément de l'output
    for i in range(len(data[0])):
        text = data[0][i][1][0]
        if re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{9}$', text):
            boites_numeriques_trouvees = True
            break
    
    if boites_numeriques_trouvees:
        for i in range(len(data[0])):
            text = data[0][i][1][0]
            if re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{9}$', text):
                numeric_boxes = data[0][i]
                return numeric_boxes[1][0]
        # Si on n'a pas trouvé de correspondance, retourner None
        return None
    else:
        points = [(227, 278), (380, 278), (380, 307), (227, 307)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return resultat2[0][0][1][0]
        
##############
        
def add_slashes(date_str):
    # Assuming the input date_str is in the format "DDMMYYYY"
    day = date_str[:2]
    month = date_str[2:4]
    year = date_str[4:]

    return f"{day}/{month}/{year}"

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
        points = [(520, 192), (659, 192), (663, 216), (520, 217)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))
        
## Delai validité 

def process_validité(data,image):
    #data = ocr.ocr(image)
    
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
                if count_dates == 2 :
                    box = data[0][i]
                    date = extract_date(box[1][0])
                    #formatted_date = date.replace(".", "/")  # Convertir . en /
                    return date
            
    else:
        points = [(518, 231), (666, 231), (666, 255), (517, 256)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(add_slashes(resultat2[0][0][1][0]))
        
## Nationalité


def process_nationalité(data, image):
    # Parcourir l'output
    boites_numeriques_trouvees = False
    nation = None

    # Parcourir les éléments dans chaque élément de l'output en ordre inverse
    for item in reversed(data[0]):
        if len(item[1][0]) == 3 and item[1][0].isupper():
            boites_numeriques_trouvees = True
            nation = item[1][0]
            break

    if boites_numeriques_trouvees:
        return nation
    else:
        points = [(345, 194), (397, 194), (397, 220), (345, 220)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        
        if len(resultat2[0]) > 0:
            return resultat2[0][0][1][0]
        else:
            return None  # Return None if both extraction methods fail


### apply ocr

corrections ={
    "FRA":"française",
    "TUN":"tunisienne"
    
}
def corriger_mot(mot, corrections):
    return corrections.get(mot, mot)

def process_image_data(image):
    data=ocr.ocr(image)
    #print(data)
    num = process_num(data,image)
    nom = process_nom(data,image) 
    prenom = process_prenom(data,image)
    naissance = process_naiss(data,image)
    validité = process_validité(data,image)
    natio = corriger_mot(process_nationalité(data,image),corrections)
    sanction = check_sanction(nom, prenom, naissance, natio)
    #sanction = 
    
    output = {
        "type":"titreSejourFRnouveau",
        "nom" : nom,
        "prenom": prenom,
        "numeroEtranger": num,
        "dateNaissance":naissance,
        "dateDelivrance": None,
        "dateValidite" : validité,
        "nationalite" : natio,
        "lieu" : None,
        "IdCin" : None,
        "sanction": sanction
        #"sanctionné":
    }

    return output

import cv2
import os

def run_sejour2(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (697, 433))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_recto{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
    output = process_image_data(cv2.imread(cropped_recto_path))
    os.remove(cropped_recto_path)
    return output



