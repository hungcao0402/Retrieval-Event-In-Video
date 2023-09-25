import json
import os
from typing import List

import meilisearch


class MeilisearchQuery:
    def __init__(self, url_meilisearch: str, ocr_index: str, frames_info: dict):
        self.client = meilisearch.Client(url_meilisearch, "mmlab")
        self.ocr_index = self.client.index(ocr_index)
        self.frames_info = frames_info
        self.asr_index = self.client.index('asr')
        
    def query_OCR(self, query: str, topk: int, matchingStrategy: str) -> List[str]:
        """
        matchinStrategy:
            all - only returns documents that contain all query terms
            last - returns documents containing all the query terms first. If there are not enough results containing all query terms to meet the requested limit

        return list keyframe name: [L01_V018/0183', 'L01_V019/0424', ...]
        """

        result = self.ocr_index.search(
            query, {"limit": topk, "matchingStrategy": matchingStrategy}
        )["hits"]

        result = [i["frame"] for i in result]

        return result

    def query_ASR(
        self,  asr_query: str, topk: int) -> list:
        # asr_list_frames = self.client.asr_list_frames

        a = self.asr_index.search(asr_query, {"limit": topk})
        hits = a["hits"]


        outputs = []
        for hit in hits:
            video_id = hit["video_id"]
            frame_start = int(hit["frame_start"])
            frame_end = int(hit["frame_end"])

            list_video_frame = self.frames_info[video_id].copy()
            list_video_frame = [int(x.split('.')[0].split('/')[-1]) for x in list_video_frame]

            list_frame_result = list(
                filter(lambda x: frame_start <= x <= frame_end, list_video_frame)
            )

            for frame_id in list_frame_result:
                keyframe_id = "{:08}".format(int(frame_id))
                outputs.append(f"{video_id}/{keyframe_id}.jpg")

        return outputs

