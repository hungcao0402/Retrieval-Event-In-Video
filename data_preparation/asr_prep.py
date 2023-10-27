import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import os 
import glob
import concurrent.futures
import tqdm
import math

save_dir = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data_preparation/asr_batch3'
def extract_mp3_from_video(input_video_path):
    video_id = os.path.basename(input_video_path).split('.')[0]
    save_path = os.path.join(save_dir,video_id)
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # Tải video vào MoviePy Clip
    video_clip = VideoFileClip(input_video_path)
    frames_per_second = video_clip.fps

    # Số lượng đoạn âm thanh MP3
    duration = math.ceil(video_clip.duration)

    # Cắt và xuất mỗi đoạn âm thanh MP3
    for start_time in tqdm.tqdm(range(0, duration, 30)):
        end_time = min(start_time + 30, duration)
        sub_clip = video_clip.subclip(start_time, end_time)

        start_frame_index = int(start_time * frames_per_second)
        end_frame_index = int(end_time * frames_per_second)
        output_mp3 = os.path.join(save_path, f"{start_frame_index}_{end_frame_index}.mp3")
        sub_clip.audio.write_audiofile(output_mp3)

if __name__ == "__main__":
    video_list = sorted(glob.glob('/mmlabworkspace/Datasets/AIC2023/Batch3/Videos/*.mp4'))[::-1]
    # extract_mp3_from_video('/mmlabworkspace/Datasets/AIC2023/Batch2/Videos/L13/L13_V008.mp4')
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        # Submit tasks for processing each video root in parallel
        futures = [executor.submit(extract_mp3_from_video, video_file) for video_file in video_list]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
