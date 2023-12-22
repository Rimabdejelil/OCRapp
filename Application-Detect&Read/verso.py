#from paddleocr import PaddleOCR
import os 
from test import ocr
import time
#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')
import re

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
    
import re
def get_bounding_rectangle(points):
    x = min(points[0][0], points[3][0])
    y = min(points[0][1], points[1][1])
    width = max(points[1][0], points[2][0]) - x
    height = max(points[2][1], points[3][1]) - y

    return x, y, width, height

def process_date(data,image):
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
                if count_dates == 2 :
                    box = data[0][i]
                    date = extract_date(box[1][0])
                    formatted_date = date.replace(".", "/")  # Convertir . en /
                    return formatted_date
                
    else:
        points = [(380, 149), (479, 148), (480, 167), (380, 169)]
        x, y, width, height = get_bounding_rectangle(points)
        cropped_image = image[y:y+height, x:x+width]
        resultat2 = ocr.ocr(cropped_image)
        if len(resultat2[0]) > 0 :
            return(resultat2[0][0][1][0])
        
def process_one(image) :
    data = ocr.ocr(image)
    emission = process_date(data,image)

    
    output = {
        "dateDelivrance" : emission
    }
    return output
from datetime import datetime
def process_two(image):
    data = ocr.ocr(image)
    expiration = process_date(data,image)
    today = datetime.now()

    # Conversion de la chaîne de date en objet de date Python
    expiration = datetime.strptime(expiration, '%d/%m/%Y')

    # Vérification de la condition
    if expiration.date() <= today.date():
        expiration = expiration.replace(year=expiration.year + 5)


    emission = process_emission(data,image)

    output ={
        "dateValidite": expiration.strftime('%d/%m/%Y'), 
        "dateDelivrance" : emission
                }
    return output
    
import cv2   

def run_verso_one(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (570, 375))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_verso_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_one(cv2.imread(cropped_recto_path))
        
        # Supprimer l'image après avoir généré la sortie
    os.remove(cropped_recto_path)
    return output

def run_verso_two(image_path,card_coordinates):
    image = cv2.imread(image_path)
    object_coordinates = [int(card_coordinates[0]), int(card_coordinates[1]), int(card_coordinates[2]), int(card_coordinates[3])]
    x1, y1, x2, y2 = object_coordinates
    img = image[y1:y2, x1:x2]
    resized_image = cv2.resize(img, (570, 375))
    # Utiliser un horodatage pour le nom du fichier
    cropped_recto_path = f"cropped_verso_{int(time.time())}.jpg"
    cv2.imwrite(cropped_recto_path, resized_image)
        
    output = process_two(cv2.imread(cropped_recto_path))
        
        # Supprimer l'image après avoir généré la sortie
    os.remove(cropped_recto_path)
    return output