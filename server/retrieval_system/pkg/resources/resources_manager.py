import glob
import json
import os

from retrieval_system.utils.io_utils import get_filename, get_filename_without_ext


class ResourcesManager:
    def __init__(self, resources_configs):
        self.resources_configs = resources_configs
        self.videos_metadata = self.load_videos_metadata()
        self.frames_metadata = self.load_frames_metadata()

    def list_all_video_ids(self, sort=True):
        if sort:
            return sorted(self.videos_metadata.keys())
        else:
            return self.videos_metadata.keys()

    def list_all_keyframe_paths_of_video_id(self, video_id, sort=True):
        assert video_id in self.list_all_video_ids(), f"Unknown video_id {video_id}"
        if sort:
            return sorted(
                glob.glob(
                    os.path.join(
                        self.resources_configs["keyframes_folder"], video_id, "*.jpg"
                    )
                )
            )
        else:
            return glob.glob(
                os.path.join(
                    self.resources_configs["keyframes_folder"], video_id, "*.jpg"
                )
            )

    def load_videos_metadata(self):
        videos_metadata = {}
        for video_metadata_file in glob.glob(
            os.path.join(self.resources_configs["videos_metadata_folder"], "*.json")
        ):
            video_id = get_filename_without_ext(video_metadata_file)
            with open(video_metadata_file, "r") as f:
                video_metadata = json.load(f)
            videos_metadata[video_id] = video_metadata
        return videos_metadata

    def load_frames_metadata(self):
        frames_metadata = {"prev_frame": {}, "next_frame": {}, "all_keyframe_idxs": {}}
        for video_id in self.list_all_video_ids():
            frames_metadata["all_keyframe_idxs"][video_id] = []
            all_keyframe_paths = self.list_all_keyframe_paths_of_video_id(video_id)
            for i, keyframe_path in enumerate(all_keyframe_paths):
                keyframe_idx = get_filename_without_ext(keyframe_path)
                keyframe_id = f"{video_id}/{get_filename(keyframe_path)}"
                frames_metadata["all_keyframe_idxs"][video_id].append(keyframe_idx)
                frames_metadata["prev_frame"][keyframe_id] = (
                    None
                    if i == 0
                    else f"{video_id}/{get_filename(all_keyframe_paths[i - 1])}"
                )
                frames_metadata["next_frame"][keyframe_id] = (
                    None
                    if i == len(all_keyframe_paths) - 1
                    else f"{video_id}/{get_filename(all_keyframe_paths[i + 1])}"
                )
        return frames_metadata

    def get_video_info(self, video_id: str) -> dict:
        assert video_id in self.list_all_video_ids(), f"Unknown video_id {video_id}"
        return self.videos_metadata[video_id]

    def get_all_keyframe_idxs_in_range(
        self, video_id: str, start_keyframe_idx: str, end_keyframe_idx: str
    ) -> list:
        assert video_id in self.list_all_video_ids(), f"Unknown video_id {video_id}"
        assert int(start_keyframe_idx) > int(
            end_keyframe_idx
        ), "start_keyframe_idx must be smaller than or equal to the end_keyframe_idx"

        all_keyframe_idxs_in_range = []
        for keyframe_idx in self.frames_metadata["all_keyframe_idxs"][video_id]:
            if int(start_keyframe_idx) <= int(keyframe_idx) <= int(end_keyframe_idx):
                all_keyframe_idxs_in_range.append(keyframe_idx)
        return all_keyframe_idxs_in_range

    def get_prev_keyframe_id(self, keyframe_id: str) -> str:
        assert (
            keyframe_id in self.frames_metadata["prev_frame"]
        ), f"Unknown keyframe_id {keyframe_id}"
        return self.frames_metadata["prev_frame"][keyframe_id]

    def get_next_keyframe_id(self, keyframe_id: str) -> str:
        assert (
            keyframe_id in self.frames_metadata["next_frame"]
        ), f"Unknown keyframe_id {keyframe_id}"
        return self.frames_metadata["next_frame"][keyframe_id]

    def get_nearby_keyframes(
        self,
        keyframe_id: str,
        num_prev_frames: int,
        num_next_frames: int,
    ) -> list:
        prev_frames = []
        next_frames = []

        current_frame = keyframe_id
        while (
            self.get_prev_keyframe_id(current_frame) is not None
            and len(prev_frames) < num_prev_frames
        ):
            current_frame = self.get_prev_keyframe_id(current_frame)
            prev_frames.append(current_frame)

        current_frame = keyframe_id
        while (
            self.get_next_keyframe_id(current_frame) is not None
            and len(next_frames) < num_next_frames
        ):
            current_frame = self.get_next_keyframe_id(current_frame)
            next_frames.append(current_frame)

        return prev_frames + [keyframe_id] + next_frames
