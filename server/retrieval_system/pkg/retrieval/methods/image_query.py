import base64

import cv2
import numpy as np


def base64_uri_to_img(uri):
    """
    > It takes a base64 encoded image and returns a numpy array of the image

    :param uri: The base64 encoded image
    :return: A numpy array of the image
    """
    encoded_data = uri.split(",")[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def query_image_by_keyframe_path(MODELS, keyframe_path, SCANN_metric="dot_product"):
    """
    > Given a keyframe path, return a list of dictionaries, each dictionary containing the video_id,
    keyframe_id, and probability of the keyframe being similar to the query keyframe

    :param MODELS: a dict of models
    :param keyframe_path: the path to the keyframe you want to query
    :param SCANN_metric: the metric used to search the SCANN index. Can be "dot_product" or "squared_l2",
    defaults to dot_product (optional)
    """
    keyframe_path += ".jpg"

    text_description_probs = {}
    outputs = []
    features = MODELS["scann"]["all_features"]
    index_map, searcher = MODELS["scann"][SCANN_metric]
    index = np.where(index_map == keyframe_path)[0][0]

    neighbors, distances = searcher.search_batched([features[index]])

    for i, img_path in enumerate(index_map[neighbors[0]][:500]):
        video_id = img_path.split("/")[0]
        keyframe_id = img_path.split("/")[1].split(".")[0]
        kf_name = f"{video_id}/{keyframe_id}"
        text_description_probs[kf_name] = float(distances[0][i])
        outputs.append(
            {
                "video_id": video_id,
                "keyframe_id": keyframe_id,
                "probs": float(distances[0][i]),
            }
        )

    return outputs


def query_image_by_file(MODELS, base64_uri, SCANN_metric):
    """
    > It takes in a base64 encoded image, encodes it, and then searches the SCANN index for the nearest
    neighbors.

    :param MODELS: a dict of models
    :param base64_uri: the base64 encoded image
    :param SCANN_metric: the metric used to search the SCANN index
    :return: A list of dictionaries, each dictionary contains the video_id, keyframe_id, and probs.
    """

    img = base64_uri_to_img(base64_uri)
    img_embedding = MODELS["encoder"].encode_image(img)
    index_map, searcher = MODELS["scann"][SCANN_metric]
    neighbors, distances = searcher.search_batched(img_embedding)

    img_probs = {}
    outputs = []

    for i, img_path in enumerate(index_map[neighbors[0]]):
        video_id = img_path.split("/")[0]
        keyframe_id = img_path.split("/")[1].split(".")[0]
        kf_name = f"{video_id}/{keyframe_id}"
        img_probs[kf_name] = float(distances[0][i])
        outputs.append(
            {
                "video_id": video_id,
                "keyframe_id": keyframe_id,
                "probs": float(distances[0][i]),
            }
        )
    return outputs
