import argparse
import os
import glob
import tqdm
import json

from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'artful-guru-401002-e73e30e04ec5.json' # Your JSON file name
client = vision.ImageAnnotatorClient()

def detect_text(path):
    """Detects text in the file."""

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.error.message:
        print('Fail!!!!!!!!!!!')
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    
    texts = response.text_annotations
    text_info_list = []
    for text in texts:
        text_info = {
            "description": text.description,
            "vertices": [
               (vertex.x,  vertex.y) for vertex in text.bounding_poly.vertices
            ]
        }
        text_info_list.append(text_info)
        
    return text_info_list

def process_video_root(video_root):
    # Place your code to process each video root here
    # For example, you can process the keyframes in this directory
    
    video_id = video_root.split('/')[-1]
    batch_id = video_root.split('/')[-4]
    
    save_dir = '/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/OCR2'
    save_path = os.path.join(save_dir, video_id+'.json')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    out_ocr = dict()
    for keyframe in tqdm.tqdm(sorted(glob.glob(os.path.join(video_root, '*.jpg')))):
        # Your keyframe processing code goes here
        keyframe_id = os.path.basename(keyframe)

        # print(keyframe_id)
        result = detect_text(keyframe)
        # # Serializing json
        out_ocr[keyframe_id] = result
        
        # Writing to sample.json
    # json_object = json.dumps(out_ocr)
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump(out_ocr, json_file, indent=4)
            
    print("Done!", save_path)

import concurrent.futures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script that demonstrates argparse.")

    # Define your command-line arguments
    parser.add_argument("--options", nargs="+", type=int, choices=[1, 2, 3], required=False,
                        help="Select one or more batch (1, 2, or 3)")
    parser.add_argument("--all", action="store_true",
                        help="Select all options (1, 2, and 3)")

    # Parse the command-line arguments
    args = parser.parse_args()
    
    keyframe_root = f'/mmlabworkspace/Datasets/AIC2023/Batch3/L36/keyframes/*'
    video_roots = sorted(glob.glob(keyframe_root))
    print(video_roots)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks for processing each video root in parallel
        futures = [executor.submit(process_video_root, video_root) for video_root in video_roots]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    # process_video_root('/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Batch2/Keyframes/L11_V010')