FROM python:3.10.4

ADD main.py .

RUN pip install mysql-connector opencv-python opencv-contrib-python tkinter

CMD ["python", "./main.py"]