from src.models import Encoder, load_meilisearch, load_SCANN_model, load_whoosh

from .load_info import load_frames_info, load_videos_info


def load_all_resources(RESOURCES_MAP):
    RESOURCES_MAP["encoder"] = Encoder()
    RESOURCES_MAP["scann"] = load_SCANN_model()
    RESOURCES_MAP["meilisearch"] = load_meilisearch()
    RESOURCES_MAP["frames_info"] = load_frames_info()
    RESOURCES_MAP["videos_info"] = load_videos_info()
