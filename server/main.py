import json
import logging
import logging.config
import os
import time
from pathlib import Path
from typing import Dict, List, Union

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrieval_system.pkg.resources.resources_manager import ResourcesManager
from retrieval_system.pkg.retrieval.core import RetrievalCore
from retrieval_system.schemas.query import TextQueryContent
from retrieval_system.utils import io_utils, logger

app_logger = logger.setup_logger("app_logger")
configs = io_utils.load_yaml_to_dict("./configs/configs.yaml")
resources_manager = ResourcesManager(configs["resources"])
search_core_configs = configs["search_core_configs"]
search_core = RetrievalCore(
    url_faiss=search_core_configs["FaissURL"],
    url_meilisarch=search_core_configs["MeiliSearchURL"],
    index_ocr=search_core_configs["index_ocr"],
)

"""
API
"""
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


@app.get("/")
async def home():
    return {"message": "Ready!"}


@app.post("/api/v1/text_query")
async def query(query_content: TextQueryContent):
    try:
        results = search_core.search_clip(
            text_query=query_content.clip_queries[0].text,
            topk=query_content.clip_queries[0].top_k,
        )
        return results["response"]
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.get("/api/v1/get_info/get_video_info")
async def get_video_info(video_id: str):
    try:
        return resources_manager.get_video_info(video_id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.get("/api/v1/get_info/frame_range")
async def get_all_keyframe_idxs_in_range(
    video_id: str, start_keyframe_idx: int, end_keyframe_idx: int
):
    try:
        return resources_manager.get_all_keyframe_idxs_in_range(
            video_id, start_keyframe_idx, end_keyframe_idx
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.get("/api/v1/get_info/prev_frame")
async def get_prev_keyframe_id(keyframe_id: str):
    try:
        return resources_manager.get_prev_keyframe_id(keyframe_id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.get("/api/v1/get_info/next_frame")
async def get_next_keyframe_id(keyframe_id: str):
    try:
        return resources_manager.get_next_keyframe_id(keyframe_id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.get("/api/v1/get_info/get_nearby_keyframes")
async def get_nearby_keyframes(keyframe_id: str):
    try:
        num_prev_frames = 24
        num_next_frames = 25
        return resources_manager.get_nearby_keyframes(
            keyframe_id, num_prev_frames, num_next_frames
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
