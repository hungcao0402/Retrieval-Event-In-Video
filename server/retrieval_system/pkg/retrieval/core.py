import logging
import os
import time
from typing import List

from ...schemas.query import TextQuery
from .methods.meilisearch_query import MeilisearchQuery
from .methods.text_query import Faiss_Clip


class RetrievalCore:
    def __init__(self, url_faiss, url_meilisarch, index_ocr,frames_info):
        self.faiss_clip = Faiss_Clip(url_faiss)
        self.meilisearch = MeilisearchQuery(url_meilisarch, index_ocr, frames_info)
    def search_clip(self, text_query: str, topk: int = 100):
        """
        Args:
            - text_query:
        Returns:
            - list[frame]
        """
        return self.faiss_clip.search(text_query, topk)

    def search_ocr(self, text_query: str, topk: int = 300) -> List[str]:
        """
        Return: list keyframe: [L01_V018/0183', 'L01_V019/0424', ...]
        """
        output = self.meilisearch.query_OCR(
            query=text_query, topk=topk, matchingStrategy="all"
        )
        return output

    def asr(self, text_query: str, topk: int = 100):
        pass

    def search(
        self,
        clip_queries: List[TextQuery] = None,
        final_top_k: int = 100,
        ocr_query: TextQuery = None,
        asr_query: TextQuery = None,
        positive_frames: List[str]=[],
        negative_frames: List[str]=[] ):
        result = {"clip": [], "ocr": [], "asr": []}
        
        if ocr_query["text"]:
            result["ocr"] = self.search_ocr(ocr_query["text"], topk=ocr_query["top_k"])
        if asr_query["text"]:
            result['asr'] = self.meilisearch.query_ASR(asr_query['text'], topk=ocr_query['top_k'])

        if clip_queries:
            if clip_queries[0]['text']:
                if len(clip_queries) > 1:
                    # return []
                    result["clip"] = self.faiss_clip.temporal_search(clip_queries)
                else:
                    if positive_frames or negative_frames:
                        result["clip"] = self.faiss_clip.search_feedback(clip_queries[0]["text"],  positive_frames, negative_frames, clip_queries[0]["top_k"])["response"]
                    else:
                        result["clip"] = self.faiss_clip.search(
                            clip_queries[0]["text"], clip_queries[0]["top_k"]
                        )["response"]

        if result["clip"] and (
            result["ocr"] or result["asr"]
        ):  # filter clip query = ocr và asr
            rs = self.filter(result["clip"], result["ocr"], result["asr"])[:final_top_k]
        elif result["clip"] and not (
            result["ocr"] or result["asr"]
        ):  # không filter clip query
            rs = result["clip"][:final_top_k]
        elif result["ocr"] and result["asr"]:  # search bằng giao ocr, asr
            rs = [frame for frame in result["ocr"] if frame in result["asr"]][:final_top_k]
        elif result["ocr"]:  # search bằng ocr
            rs = result["ocr"][:final_top_k]
        else:  # search bằng asr
            rs = result["asr"][:final_top_k]

        print('Before:', len(rs))
        rs = self.filter_nearframe(rs)
        print('After:', len(rs))

        return rs

    def filter(self, frames1, frames2=[], frames3=[]):
        if frames3 and frames2:
            frames_filter = [frame for frame in frames2 if frame in frames3]
        else:
            frames_filter = frames2 if frames2 else frames3
        result = [frame for frame in frames1 if frame in frames_filter]
        return result


    def filter_nearframe(self, list_key_frame):
        # Tạo một dictionary để lưu trữ các phần tử có cùng id trước '/'
        result = []

        video_dict = {}

        for i, kf1 in enumerate(list_key_frame):
            video_id1 = kf1.split('/')[0]
            id1 = int(kf1.split('/')[1].split('.')[0])

            if video_id1 not in video_dict:
                video_dict[video_id1] = [kf1]
                result.append(kf1)
            else:  
                flag = True
                for kf2 in video_dict[video_id1]:
                    id2 = int(kf2.split('/')[1].split('.')[0])
                    if abs(id1-id2) < 75:
                        flag=False
                if flag:
                    result.append(kf1)
                    video_dict[video_id1].append(kf1)
        
        return result
