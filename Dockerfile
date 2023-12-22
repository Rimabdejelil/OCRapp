
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements_cpu.txt ./
COPY app.py detect_and_crop1.py CIN_TN.py Card_ID_ancien2.py PASSEPORT2.py PasseportTun.py Sejour2.py SejourAncien.py ID_FR2.py sanct.py test.py tt.py verso.py  best.pt ./
COPY utils ./utils
COPY templates ./templates
COPY static ./static
COPY models ./models

RUN pip install flask 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_cpu.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx libgomp1 libglib2.0-0
RUN pip install -U check_orientation
RUN python -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+

RUN pip install prometheus-client

EXPOSE 5000

CMD ["python3", "-m", "app", "run", "--host=0.0.0.0"]




