from app import process_image
image_path = 'C:/Users/rimba/Desktop/293.py'
detection_type = 'recto'
options = {}
result, card_class = process_image(image_path, detection_type, options)