from PIL import Image
import os

def compress_image(input_path, output_path, quality=50):
    """
    Nén ảnh với chất lượng cụ thể.

    Args:
        input_path (str): Đường dẫn đến ảnh gốc.
        output_path (str): Đường dẫn đến ảnh sau khi nén.
        quality (int): Chất lượng nén (0 - 100), giá trị càng thấp càng nén mạnh.

    Returns:
        None
    """
    try:
        image = Image.open(input_path)
        image.save(output_path, optimize=True, quality=quality)
        # print(f"Đã nén ảnh thành công: {output_path}")
    except Exception as e:
        print(input_path)
        print(f"Lỗi: {str(e)}")



import os
import multiprocessing
import tqdm
import glob

def process_folder(folder_path):
    os.mkdir(folder_path.replace('Keyframe',  'Keyframe_Compress'))
    for img_path in tqdm.tqdm(glob.glob(os.path.join(folder_path, '*'))):
        output_image_path = img_path.replace('Keyframe', 'Keyframe_Compress')
        compress_image(img_path, output_image_path, quality=50)

def process_all_folders(root_folder):
    folders = [os.path.join(root_folder, folder_name) for folder_name in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder_name))]

    # Create a pool of worker processes
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Process each folder concurrently
    pool.map(process_folder, folders)

if __name__ == "__main__":
    root_directory = "/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Keyframe"

    process_all_folders(root_directory)

    # print('original',len(glob.glob("/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Keyframe/*/*.jpg")))
    # print('after',len(glob.glob("/mmlabworkspace/Students/AIC/MMLAB-UIT-AIC2023/data/Merge/Keyframe_Compress/*/*.jpg")))

