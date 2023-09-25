FROM python:3.9.18-bullseye

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app/server

COPY . .

RUN pip install -r requirements.txt

RUN pip install -e .
ENV TZ=Asia/Ho_Chi_Minh

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
