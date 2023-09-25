import os
import time
import requests
import yaml
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from retrieval_system.pkg.retrieval.core import RetrievalCore
from retrieval_system.schemas.query import TextQueryContent
from retrieval_system.utils.load_info import get_index, load_frame_info, load_videos_info
from retrieval_system.utils.logger import Log

logger = Log('server')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'configs/aic2023-398508-d971b8edb159.json' 

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


@app.post("/search")
async def search(text_data: TextQueryContent):
    start = time.time()
    print(text_data.dict())
    keyframes = search_core.search(**text_data.dict())
    result = [os.path.join("Keyframe", i) for i in keyframes]

    time_query = time.time()-start
    Log().log.info(f"Time: {time_query} | Query: {text_data.dict()}")

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
    Log().log.info(f"filename: {image.filename}")
    # Xử lý hình ảnh ở đây, sau đó gửi đến app2
    # with open(image.filename, "wb") as f:
    #     f.write(image.file.read())
    # files = {"file": (file.filename, file.file)}
    response = requests.post(config['FaissURL'].replace('text_query','query_by_img'), files={"file": (image.filename, image.file)}).json()
    result = [os.path.join("Keyframe", i) for i in response['response']]

    return {"result": result}

# @app.post("/clip_query")
# async def clip_query(query: str, topk: int):
#     start = time.time()
#     result = search_core.search_clip(text_query=query, topk=topk)
#     keyframes = result["response"]
#     distances = result["distances"]
#     keyframes = [os.path.join("Keyframe", i) for i in keyframes]
#     print("Time:", time.time() - start)
#     return {"result": keyframes, "distances": distances}


# @app.post("/ocr_query")
# async def ocr_query(query, topk: int = 300):
#     start = time.time()
#     result = search_core.search_ocr(text_query=query, topk=topk)
#     result = [os.path.join("Keyframe", i) for i in result]
#     print("Time:", time.time() - start)
#     return {"result": result}


