#<import redis
#import io
#import joblib
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True,lang='fr')
#redis_host = 'localhost'
#redis_port = 6379

#det_model_dir = '/root/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer/ch_PP-OCRv4_det_infer.tar'
#rec_model_dir = '/root/.paddleocr/whl/rec/latin/latin_PP-OCRv3_rec_infer'
#cls_model_dir = '/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'

#r = redis.Redis(host=redis_host, port=redis_port)


#def load_model_from_directory(model_dir):
 #   model_key = f'model_{model_dir}'
  #  if r.exists(model_key):
   #     return r.get(model_key).decode('utf-8')
    #else:
     #   r.set(model_key, model_dir)
    #return model_dir
#
#cached_det_model_dir = load_model_from_directory(det_model_dir)
#cached_rec_model_dir = load_model_from_directory(rec_model_dir)
#cached_cls_model_dir = load_model_from_directory(cls_model_dir)

#def initialize_paddleocr(det_model_dir, rec_model_dir, cls_model_dir):

 #   ocr = PaddleOCR(
  #      det_model_dir=det_model_dir,
#
 #       rec_model_dir=rec_model_dir,

  #      cls_model_dir=cls_model_dir,

   #     use_angle_cls=True,  # Réglez d'autres paramètres selon vos besoins

    #    lang='fr'
     #   )

    #return ocr

#ocr = initialize_paddleocr(cached_det_model_dir, cached_rec_model_dir, cached_cls_model_dir)




