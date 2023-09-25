import glob
import json
import os


def load_videos_info(path='/app/server/data/Merge/Metadata'):
    print("Loading videos info...")
    youtube_urls = dict()
    for file in glob.glob(os.path.join(path,'*.json')):
        video_id = file.split('.')[0].split('/')[-1]
        with open(file, 'r') as json_file:
            data = json.load(json_file)
        youtube_urls[video_id] = data['watch_url']
    return youtube_urls


def load_frame_info(KEYFRAMES_FOLDER):
    frames_info = dict()

    for video_folder in sorted(glob.glob(os.path.join(KEYFRAMES_FOLDER, "*"))):
        video_id = os.path.basename(video_folder)
        all_frame = sorted(glob.glob(os.path.join(video_folder, "*.jpg")))
        all_frame = ["/".join(file_path.split("/")[-2:]) for file_path in all_frame]
        frames_info[video_id] = all_frame
    return frames_info


def get_index(frames_info, keyframe):
    video_id = keyframe.split("/")[-2]
    all_frame = frames_info[video_id]
    keyframe = "/".join(keyframe.split("/")[-2:])  # L01_V002/0248.jpg
    try:
        frame_index = all_frame.index(keyframe)
    except ValueError:
        return None  # Trả về None nếu phần tử mục tiêu không tồn tại trong danh sách

    return all_frame, frame_index


def test():
    f = load_frame_info(
        "/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Batch1/Keyframes"
    )
    result = get_index(f, "L01_V002/0248.jpg")
    return result


# # extract video_id
# sub_path1 = os.path.dirname(full_path)  # Lấy thư mục cha của đường dẫn hiện tại
# sub_path2 = os.path.basename(os.path.dirname(full_path))  # Lấy tên thư mục con của đường dẫn hiện tại
# video_id = os.path.join(sub_path1, sub_path2)  # Kết hợp lại thành đường dẫn mới

# # extract keyframe_id
# file_name = os.path.basename(full_path)


def load_frames_info():
    print("Loading frames info...")
    frames_info = {"prev_frame": {}, "next_frame": {}, "all_frames": {}}
    for video_root in sorted(
        glob.glob(os.path.join(os.environ["KEYFRAMES_FOLDER"], "*/"))
    ):
        video_id = os.path.basename(os.path.normpath(video_root))
        frames_info["all_frames"][video_id] = []
        all_keyframe_paths = sorted(glob.glob(os.path.join(video_root, "*.jpg")))
        for i in range(len(all_keyframe_paths)):
            keyframe_id = os.path.basename(all_keyframe_paths[i]).split(".")[0]
            frames_info["all_frames"][video_id].append(keyframe_id)
            frames_info["prev_frame"][f"{video_id}/{keyframe_id}"] = (
                None
                if i == 0
                else os.path.basename(all_keyframe_paths[i - 1]).split(".")[0]
            )
            frames_info["next_frame"][f"{video_id}/{keyframe_id}"] = (
                None
                if i == len(all_keyframe_paths) - 1
                else os.path.basename(all_keyframe_paths[i + 1]).split(".")[0]
            )
    return frames_info
