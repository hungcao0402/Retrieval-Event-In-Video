import numpy as np
import os
import glob
import json
import pandas as pd
import tqdm

def stack_features(data_root: str, feature_name: str, model_name: str, output_dir, feature_dim=512) -> np.array:
    """Stack all features to a file

    Args:
        data_root (str): Data root directory
        feature_name (str): Feature name (CLIP_Features, BLIP_Features, ...). Must match directory name
        model_name (str): Model name of feature (ViT_B16, ViT_B32). Must match directory name
        output_dir (path): Output directory
        feature_dim (str, optional): Feature dimension. Defaults to 512 (CLIP-ViT/B16).

    Returns:
        np.array: (num_features, feature_dim)
    """
    
    feature_files = sorted(glob.glob(f'{data_root}/Batch*/{feature_name}/{model_name}/*.npy'))   
    stacked_features = []
    for feature_file in feature_files:
        feature = np.load(feature_file)
        stacked_features.append(feature)
    stacked_features = np.concatenate(stacked_features, axis=0)

    print('stacked_features shape:', stacked_features.shape)
    
    save_path = os.path.join(output_dir, feature_name + '_' + model_name + '_' + '.npy')
    np.save(save_path, stacked_features)
    
    return stacked_features
        
        
def stack_keyframe_names(data_root: str, output_dir: str) -> list:
    """compose keyframe names to json file

    Args:
        data_root (str): _description_
        output_dir (str): _description_

    Returns:
        list: keyframe_names list
    """
    keyframe_names = sorted(glob.glob(f'{data_root}/*/Keyframes/*/*/*.jpg'))
    
    print('Number of files:', len(keyframe_names))
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'keyframe_names')
    with open(output_path, 'w') as f:
        json.dump(keyframe_names, f)
        
    return keyframe_names


data_root = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data'
feature_name = 'BLIP_Features'
model_name = 'Projected_Feature'
output_dir = 'faiss/data/faiss_database'

# stack_features(data_root, feature_name, model_name, output_dir)
# stack_keyframe_names(data_root, output_dir)

def create_feature_and_path_file(data_path='/mmlabworkspace/Datasets/AIC2023', feature_folder='CLIP_Features/ViT_B32', save_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Feature_data/ViT_B32'):
    map_keyframes = sorted(glob.glob(os.path.join(data_path, 'Batch*','Map_Keyframes','*.csv')))

    frame_ids = []
    features = []
    
    for file_path in tqdm.tqdm(map_keyframes):
        video_id = os.path.basename(file_path).split('.')[0]
        if video_id == 'L20_V010':
            continue
        data = pd.read_csv(file_path)

        frame_idx_list = data['frame_idx'].tolist()
        frame_idx_list = [os.path.join(video_id, str(i).zfill(8)+'.jpg') for i in frame_idx_list]
        frame_ids.extend(frame_idx_list)
        # cho idx gốc
        # frame_idx_list = data['frame_idx'].tolist()
        # frame_idx_list = [os.path.join(video_id, str(i).zfill(8)) for i in frame_idx_list]
        
        #process feature
        feature_video_path = file_path.replace('Map_Keyframes', feature_folder).replace('.csv', '.npy')
        feature = np.load(feature_video_path)
        features.append(feature) ####### blip 

    features = np.concatenate(features, axis=0)

    print('stacked_features shape:', features.shape)
    
    print('frame_ids len:', len(frame_ids))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Directory '{save_path}' created.")
    else:
        print(f"Directory '{save_path}' already exists.")

    np.save(os.path.join(save_path, 'feature.npy'), features)
    with open(os.path.join(save_path, 'keyframe_name.json'), 'w') as file:
        json.dump(frame_ids, file)

def BLIP_create_feature_and_path_file(data_path='/mmlabworkspace/Datasets/AIC2023', feature_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data_preparation/BLIP_768', save_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Feature_data/ViT_B32'):
    map_keyframes = sorted(glob.glob(os.path.join(data_path, 'Batch*','Map_Keyframes','*.csv')))

    frame_ids = []
    features = []
    for file_path in tqdm.tqdm(map_keyframes):
        video_id = os.path.basename(file_path).split('.')[0]
        if video_id == 'L20_V010':
            continue
        data = pd.read_csv(file_path)

        frame_idx_list = data['frame_idx'].tolist()
        frame_idx_list = [os.path.join(video_id, str(i).zfill(8)+'.jpg') for i in frame_idx_list]
        frame_ids.extend(frame_idx_list)

        #process feature
        feature_video_path = os.path.join(feature_path, video_id+'.npy')

        feature = np.load(feature_video_path)

        ####### BLIP
        features.append(feature[:,0,:,:]) ####### blip 
        ####### BLIP
    features = np.concatenate(features, axis=0)

    print('stacked_features shape:', features.shape)
    
        
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Directory '{save_path}' created.")
    else:
        print(f"Directory '{save_path}' already exists.")

    np.save(os.path.join(save_path, 'feature.npy'), features)
    with open(os.path.join(save_path, 'keyframe_name.json'), 'w') as file:
        json.dump(frame_ids, file)

if __name__ == "__main__":

    # feature_folder = 'BLIP_Features/Feature_768'
    # save_path='/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Feature_data/BLIP_768'
    # data_root = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data'

    # create_feature_and_path_file(data_path=data_root,feature_folder= feature_folder, save_path= save_path)

    create_feature_and_path_file()
