import os
import glob
import nibabel as nib
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from label_systems import (
    AEval_label, 
    FLARE22_label, 
    AMOS_label, 
    WORD_label, 
    TotalSeg_label, 
    TotalSegMR_label, 
    BTCV_label
)

# 自动生成映射关系
def create_mapping(label_system):
    return {v: AEval_label.get(k, 0) for k, v in label_system.items()}

def create_mapping(label_system):
    return {v: AEval_label[k] for k, v in label_system.items() if AEval_label.get(k, 0) != 0}


def process_file(filename, input_folder, output_folder, mapping):
    # 读取标签文件
    file_path = os.path.join(input_folder, filename)
    img = nib.load(file_path)
    data = img.get_fdata()
    # 创建 A_Eval 标签数据
    a_eval_data = np.zeros_like(data, dtype=np.uint8)
    # 映射标签
    for label, a_eval_label in mapping.items():
        a_eval_data[data == label] = a_eval_label

    # 保存转换后的 A_Eval 标签数据
    a_eval_img = nib.Nifti1Image(a_eval_data, img.affine, img.header)
    output_file_path = os.path.join(output_folder, filename)
    nib.save(a_eval_img, output_file_path)

# 文件夹路径
input_base_folder = 'predict_results_raw/*' 
output_base_folder = 'predict_results_converted/'

# input_base_folder = 'gts_raw/*' 
# output_base_folder = 'gts_converted/'

# 获取所有子文件夹路径
input_folders = glob.glob(input_base_folder)

# 遍历每个子文件夹
for input_folder in input_folders:
    # 获取文件夹名称
    folder_name = os.path.basename(input_folder)
    output_folder = os.path.join(output_base_folder, folder_name)

    # 检查目标文件夹是否存在且包含相同数量的 .nii.gz 文件
    if os.path.exists(output_folder):
        existing_files = [f for f in os.listdir(output_folder) if f.endswith('.nii.gz')]
        input_files = [f for f in os.listdir(input_folder) if f.endswith('.nii.gz')]
        if len(existing_files) == len(input_files):
            print(f"文件夹 {folder_name} 已经处理过，跳过转换。")
            continue

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 根据文件夹名字的前缀判断使用的映射
    prefix = folder_name.split('_')[0]
    mapping = None

    print(prefix)

    if prefix == 'FLARE22':
        mapping = create_mapping(FLARE22_label)
    elif prefix == 'AMOSCT' or prefix == 'AMOSMR' or prefix == 'AMOSCTMR':
        mapping = create_mapping(AMOS_label)
    elif prefix == 'WORD':
        mapping = create_mapping(WORD_label)
    elif prefix == 'TotalSeg':
        mapping = create_mapping(TotalSeg_label)
    elif prefix == 'TotalSegMR':
        mapping = create_mapping(TotalSegMR_label)
    elif prefix == 'BTCV':
        mapping = create_mapping(BTCV_label)
    else:
        print(f"未找到合适的映射体系: {folder_name}")
        continue

    print(mapping)

    # 获取所有 .nii.gz 文件
    filenames = [f for f in os.listdir(input_folder) if f.endswith('.nii.gz')]

    # 使用线程池处理文件
    with ThreadPoolExecutor(max_workers=8) as executor:
        def process_if_not_exists(filename):
            output_file_path = os.path.join(output_folder, filename)
            # 如果文件已经存在，跳过该文件
            if os.path.exists(output_file_path):
                return
            process_file(filename, input_folder, output_folder, mapping)
        
        list(tqdm(executor.map(process_if_not_exists, filenames), total=len(filenames)))