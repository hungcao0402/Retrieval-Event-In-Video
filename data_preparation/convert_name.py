import os
import glob
import pandas as pd
import tqdm
# Đường dẫn đến thư mục chứa các tệp cần đổi tên
path_kf='/mmlabworkspace/Datasets/AIC2023/Batch3/L36/keyframes'

path_map = '/mmlabworkspace/Datasets/AIC2023/Batch3/Map_Keyframes'

max =0 
# Lặp qua tất cả các tệp trong thư mục
for video in tqdm.tqdm(sorted(glob.glob(os.path.join(path_kf,'*')))):
    video_id = os.path.basename(video)

    data_map = pd.read_csv(os.path.join(path_map, video_id+'.csv'))
    for index, row in data_map.iterrows():
        frame_path = os.path.join(path_kf, video_id,str(int(row['n'])).zfill(3) + '.jpg')

        new_path = os.path.join(path_kf, video_id, str(int(row['frame_idx'])).zfill(8) + '.jpg')
        os.rename(frame_path, new_path)

