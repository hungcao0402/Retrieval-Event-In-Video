import json
import os
import time
from bisect import bisect, bisect_left
from typing import List

import numpy as np
import requests
from tqdm import tqdm
from ....utils.translate import translate_text

class Faiss_Clip:
    def __init__(self, url):
        self.url = url

    def search(self, text_query, topk=10) -> List[str]:
        """
        # return
            {
                "response": [L01_V018/0183', 'L01_V019/0424', ...],
                "distances": }
            }
        """
    # if text_query[0] == '!':
        text_query = translate_text(target='en', text=text_query)['translatedText']

        params = {"text_query": text_query, "topk": topk}
        headers = {"accept": "application/json"}

        response = requests.post(self.url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None

    def search_feedback(self, text_query, positive_frames=[], negative_frames=[], topk=10) -> List[str]:
        """
        # return
            {
                "response": [L01_V018/0183', 'L01_V019/0424', ...],
                "distances": }
            }
        """
        text_query = translate_text(target='en', text=text_query)['translatedText']

        positive_frames = ['/'.join(x.split('/')[-2:]) for x in positive_frames]
        negative_frames = ['/'.join(x.split('/')[-2:]) for x in negative_frames]

        url = self.url.replace('text_query', 'relevance_feedback')
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        data = {
            "text_query": text_query,
            "pos_list": positive_frames,
            "neg_list": negative_frames,
            "topk": topk
        }
        
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None



    def temporal_search(self, list_text_query: list):

        list_result = []
        for query in list_text_query:
            list_result.append(self.search(query["text"], topk=query["top_k"])['response'])
        outputs = []

        if len(list_text_query) == 2:

            for frame1 in list_result[0]:
                for frame2 in list_result[1]:
                    video_id1, frame_id1 = frame1.split("/")
                    video_id2, frame_id2 = frame2.split("/")
                    if (
                        video_id1 == video_id2
                        and 50
                        <= int(frame_id2.split(".")[0]) - int(frame_id1.split(".")[0])
                        < 800
                    ):
                        outputs.append(frame1)
                        outputs.append(frame2)
        if len(list_text_query) == 3:
            for frame1 in list_result[0]:
                video_id1, frame_id1 = frame1.split("/")
                for frame2 in list_result[1]:
                    video_id2, frame_id2 = frame2.split("/")
                    if video_id1 == video_id2 and (
                        1
                        <= int(frame_id2.split(".")[0]) - int(frame_id1.split(".")[0])
                        < 1000
                    ):
                        for frame3 in list_result[2]:
                            video_id3, frame_id3 = frame3.split("/")
                            if (
                                video_id2 == video_id3
                                and 1
                                <= abs(
                                    int(frame_id3.split(".")[0])
                                    - int(frame_id2.split(".")[0])
                                )
                                < 1000
                            ):
                                outputs.append(frame1)
                                outputs.append(frame2)
                                outputs.append(frame3)
        return outputs
