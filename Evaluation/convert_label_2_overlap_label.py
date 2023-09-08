import os
import SimpleITK as sitk
import numpy as np
from tqdm import tqdm
from label_systems import FLARE_label, AMOS_label, WORD_label, TotalSeg_label, BTCV_label, overlap_label

def generate_label_map(label_dict, target_label_dict):
    target_value = {v: k for k, v in target_label_dict.items()}
    return {k: target_value[v] for k, v in label_dict.items() if v in target_value}

def convert_folder(original_seg_folder, prediction_folders_raw_path, prediction_folders_converted_path, label_map):
    if not os.path.exists(os.path.join(prediction_folders_converted_path, original_seg_folder)):
        os.makedirs(os.path.join(prediction_folders_converted_path, original_seg_folder))

    for seg_file in tqdm(os.listdir(os.path.join(prediction_folders_raw_path, original_seg_folder))):
        if '.nii.gz' not in seg_file:
            continue
        seg_sitk = sitk.ReadImage(os.path.join(prediction_folders_raw_path, original_seg_folder, seg_file))
        seg = sitk.GetArrayFromImage(seg_sitk)
        converted = np.zeros_like(seg, dtype=seg.dtype)

        for label in label_map:
            converted[seg == int(label)] = int(label_map[label])
        
        converted_sitk = sitk.GetImageFromArray(converted.astype(np.uint8))
        converted_sitk.SetSpacing(seg_sitk.GetSpacing())
        converted_sitk.SetOrigin(seg_sitk.GetOrigin())
        converted_sitk.SetDirection(seg_sitk.GetDirection())
        sitk.WriteImage(converted_sitk, os.path.join(prediction_folders_converted_path, original_seg_folder, seg_file))

def main():
    prediction_folders_raw_path = 'predict_results'
    prediction_folders_converted_path = 'predict_folders_converted_to_overlap'
    # prediction_folders_raw_path = 'gtsVal_raw'
    # prediction_folders_converted_path = 'gtsVal_overlap_label'
    
    print(f"Converting all segmentation results from subfolders in {prediction_folders_raw_path} to subfolders in {prediction_folders_converted_path}.")

    label_maps = {
        'FLARE': generate_label_map(FLARE_label, overlap_label),
        'AMOS': generate_label_map(AMOS_label, overlap_label),
        'WORD': generate_label_map(WORD_label, overlap_label),
        'TotalSeg': generate_label_map(TotalSeg_label, overlap_label),
        'BTCV': generate_label_map(BTCV_label, overlap_label)
    }

    prediction_folders = os.listdir(prediction_folders_raw_path)

    for original_seg_folder in prediction_folders:
        
        for prefix, label_map in label_maps.items():
            if original_seg_folder.startswith(prefix):
                print(f"Converting label system of {prefix} to overlap label system")
                for k, v in label_map.items():
                    print(f"{FLARE_label[v]}: {k} -> {v}")
                
                convert_folder(original_seg_folder, prediction_folders_raw_path, prediction_folders_converted_path, label_map)
                break
        else:
            print(f"The label system of {original_seg_folder} is not known. Skipping conversion.")

if __name__ == '__main__':
    main()
