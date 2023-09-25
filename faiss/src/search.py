import numpy as np
import faiss
import json
from fastapi import FastAPI, UploadFile
from modules import Encoder, Faiss
import argparse
import uvicorn
from pydantic import BaseModel
import yaml
import time
from utils import Log
from PIL import Image
import io

from pydantic import BaseModel
from typing import List

class RelevanceFeedbackInput(BaseModel):
    text_query: str
    pos_list: List[str]
    neg_list: List[str]
    topk: int

logger = Log('faiss_service')

TEXT_SEARCH_API_PORT = 8000

class TextSearchApi:
    def __init__(self, config_file_path):
        with open(config_file_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.app = FastAPI()
        self.database = np.load(self.config['feature_path'])
        print('database shape:', self.database.shape)

        self.encoder = Encoder(model_name=self.config['model_clip'], project= self.config['project_blip'], use_gpu=self.config['use_gpu'])
        self.faiss_searcher = Faiss(self.config['feature_path'],  use_gpu=self.config['use_gpu'])
        with open(self.config['keyframe_name_path']) as f:
            self.keyframe_names = json.load(f)

        @self.app.get("/")
        async def root():
            return {"message": "hello"}

        @self.app.post("/text_query")
        async def search(text_query: str, topk: int):
            queries = np.array([text_query])
            
            t0 = time.time()
            encoded_text = self.encoder.encode_texts(queries)
            t1 = time.time()
            
            print(encoded_text.shape)
            distances, result_indices = self.faiss_searcher.search(encoded_text, top_k=topk)
            t2 = time.time()
            
            Log().log.info(f"Total time: {t2-t0} | Encode time: {t1-t0} | Faiss time: {t2-t1} | Query: {text_query}")

            result = [self.keyframe_names[i] for i in result_indices.ravel()]
            
            return {"response": result, 
                    "distances": distances.ravel().tolist()
            }

        @self.app.post("/query_by_kf_id")
        async def search_by_id(keyframe_id: str, topk: int):
            idx = self.keyframe_names.index(keyframe_id)
            feature_kf = self.database[idx]

            distances, result_indices = self.faiss_searcher.search(np.expand_dims(feature_kf, axis=0), top_k=topk)
            result = [self.keyframe_names[i] for i in result_indices.ravel()]

            return {"response": result, 
                    "distances": distances.ravel().tolist()
            }

        @self.app.post("/relevance_feedback")
        async def relevance_feedback( input_data: RelevanceFeedbackInput):
            text_query = input_data.text_query
            pos_list = input_data.pos_list
            neg_list = input_data.neg_list
            topk = input_data.topk


            id_pos = np.where(np.isin(self.keyframe_names, pos_list))[0]
            id_neg = np.where(np.isin(self.keyframe_names, neg_list))[0]
            
            feature_pos = self.database[id_pos]
            feature_neg = self.database[id_neg]

            queries = np.array([text_query])

            encoded_text = self.encoder.encode_texts(queries)

            if len(feature_pos) and len(feature_neg):
                new_query_feature = encoded_text[0] + 1 *  (1 / len(feature_pos)) * np.sum(feature_pos, axis=0) - 0.3 * (1 / len(feature_neg)) * np.sum(feature_neg, axis=0)
            elif len(feature_pos):
                new_query_feature = encoded_text[0] +  (1 / len(feature_pos)) * np.sum(feature_pos, axis=0)
            else:
                new_query_feature = encoded_text[0] +  (1 / len(feature_neg)) * np.sum(feature_neg, axis=0)
            
            new_query_feature = np.expand_dims(new_query_feature, axis=0)
            distances, result_indices = self.faiss_searcher.search(new_query_feature, top_k=topk)

            result = [self.keyframe_names[i] for i in result_indices.ravel()]

            return {"response": result, 
                    "distances": distances.ravel().tolist()
            }


        @self.app.post("/query_by_img")
        async def query_by_img(file: UploadFile):
            image_bytes = await file.read()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            feature = self.encoder.encode_image(image)
            distances, result_indices = self.faiss_searcher.search(feature, top_k=200)
            result = [self.keyframe_names[i] for i in result_indices.ravel()]

            return {"response": result, 
                    "distances": distances.ravel().tolist()
            }

    def run(self, port):
        uvicorn.run(self.app, host="0.0.0.0", port=port)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--config-path", type=str)
    
    parser.add_argument("--port", type=int, default=TEXT_SEARCH_API_PORT)
    args = parser.parse_args()

    api = TextSearchApi(config_file_path=args.config_path)
    api.run(port=args.port)
