import os
import time
import requests
import yaml
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from retrieval_system.pkg.retrieval.core import RetrievalCore
from retrieval_system.schemas.query import TextQueryContent
from retrieval_system.utils.load_info import get_index, load_frame_info, load_videos_info
from retrieval_system.utils.logger import get_Log

logger = get_Log('server')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'configs/artful-guru-401002-e73e30e04ec5.json' 

with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)
frame_info = load_frame_info("/app/server/data/Keyframe")
youtube_urls = load_videos_info('/app/server/data/Metadata')

app = FastAPI(
    title="MMLAB-UIT-AIC2023",
    description="This is the API we are using at HCMC AI Challenge 2023",
    version="v0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_core = RetrievalCore(
    url_faiss=config["FaissURL"],
    url_meilisarch=config["MeiliSearchURL"],
    index_ocr=config["index_ocr"],
    frames_info=frame_info)

logger_question = get_Log('question')

@app.post("/search")
async def search(text_data: TextQueryContent):
    start = time.time()
    print(text_data.dict())
    print()
    try:
        if text_data.dict()['clip_queries']:
            if text_data.dict()['clip_queries'][0]['text'][0] == ',':
                text_data.clip_queries[0].text = text_data.dict()['clip_queries'][0]['text'][1:]
                logger_question.info(text_data.dict()['clip_queries'][0]['text'] )
    except:
        print('error')

    keyframes = search_core.search(**text_data.dict())
    result = [os.path.join("Keyframe", i) for i in keyframes]

    time_query = time.time()-start
    logger.info(f"Time: {time_query} | Query: {text_data.dict()}")

    return {"result": result}

@app.post("/keyframe_search")
async def keyframe_search(frame, topk=100):
        """
        # return
            {
                "response": [L01_V018/0183.jpg', 'L01_V019/0424.jpg', ...],
                "distances": 
            }
        """
        name = '/'.join(frame.split('/')[-2:])
        params = {"keyframe_id": name, "topk": topk}
        headers = {"accept": "application/json"}
        video_id = name.split('/')[0]
        frame_index = frame.split('/')[-1].split('.')[0]
        

        # Log().log.info(f"keyframe_search: {frame}")

        response = requests.post(config['FaissURL'].replace('text_query','query_by_kf_id'), params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            similar_keyframes = [os.path.join("Keyframe", i) for i in data['response']]

            near_by_keyframes, index = get_index(frame_info, frame)
            near_by_keyframes = [os.path.join("Keyframe", i) for i in near_by_keyframes]

            return {"near_by_keyframes": near_by_keyframes, 
                    "index": index,
                    "youtube_url": youtube_urls[video_id],
                    "played_second": int(int(frame_index)/25),
                    "similar_keyframes": similar_keyframes
                    }

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None

@app.post("/image_search/")
async def image_search(image: UploadFile):
    logger.info(f"filename: {image.filename}")
    # Xử lý hình ảnh ở đây, sau đó gửi đến app2
    # with open(image.filename, "wb") as f:
    #     f.write(image.file.read())
    # files = {"file": (file.filename, file.file)}
    response = requests.post(config['FaissURL'].replace('text_query','query_by_img'), files={"file": (image.filename, image.file)}).json()
    result = [os.path.join("Keyframe", i) for i in response['response']]

    return {"result": result}


@app.post("/submit")
async def image_search(frame):

    # Địa chỉ URL của endpoint login
    url = "https://eventretrieval.one/api/v1/login"

    # Dữ liệu JSON chứa tên người dùng và mật khẩu
    data = {
        "username": "mmlabuit",
        "password": "Caipha4a"
    }

    # Thực hiện yêu cầu POST
    response = requests.post(url, json=data)

    # Kiểm tra phản hồi
    if response.status_code == 200:
        # Yêu cầu thành công, bạn có thể xử lý dữ liệu phản hồi ở đây
        print("Login successful")
        sessionId = response.json()['sessionId']  # Dữ liệu JSON phản hồi từ server


        # Define the URL
        url = "https://eventretrieval.one/api/v1/submit"

        frame = '/'.join(frame.split('.')[0].split('/')[-2:])

        video_id, frame = frame.split('/')

        # Define the parameters
        params = {
            "item": video_id,
            "frame": frame,
            "session": sessionId
        }

        # Send the GET request
        response = requests.get(url, params=params)

        # logging.info(f"Request Parameters: {params}")
        logger.info(f"filename: {params}")
        # Check if the request was successful (status code 200)
        logger.info(f"filename: {response.json()}")
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            description = data.get("description")
            submission_status = data.get("status")
            # logging.info(f"Response Description: {description}")
            # logging.info(f"Response Submission Status: {submission_status}")
            print("Description:", description)
            print("Submission Status:", submission_status)
        else:
            error_message = f"Failed to retrieve data. Status code: {response.status_code}"
            # logging.error(error_message)
            print(error_message)

        return response.json()
    else:
        # Yêu cầu không thành công, hiển thị thông báo lỗi
        print(f"Login failed. Status code: {response.status_code}")
        print(response.text)  # In nội dung phản hồi để xem lý do thất bại (nếu có)
        return response.json()

