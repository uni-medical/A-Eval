from collections import defaultdict
import os
import glob
import nibabel as nib
import numpy as np
import json
import csv
from tqdm import tqdm
from SurfaceDice import compute_surface_distances, compute_surface_dice_at_tolerance, compute_dice_coefficient


# label_tolerance = OrderedDict({'Liver': 5, 'RK':3, 'Spleen':3, 'Pancreas':5, 
#                    'Aorta': 2, 'IVC':2, 'RAG':2, 'LAG':2, 'Gallbladder': 2,
#                    'Esophagus':3, 'Stomach': 5, 'Duodenum': 7, 'LK':3})
label_tolerance = [0,5,3,3,5,2,2,2,2,2,3,5,7,3]

def process_results(prediction_folder, gt_folder, class_list):
    print(prediction_folder)
    print(gt_folder)
    total_dsc = defaultdict(int)
    total_nsd = defaultdict(int)
    count = defaultdict(int)
    case_dsc = defaultdict(list)
    case_nsd = defaultdict(list)
    
    prediction_files = glob.glob(os.path.join(prediction_folder, '*.nii.gz'))
    for prediction_file in tqdm(prediction_files, desc='Processing', unit=' file'):
        filename = os.path.basename(prediction_file)
        gt_file = os.path.join(gt_folder, filename)
        gt_nii = nib.load(gt_file)
        case_spacing = gt_nii.header.get_zooms()

        if os.path.exists(gt_file):
            prediction = nib.load(prediction_file).get_fdata().astype(np.uint8)
            gt = nib.load(gt_file).get_fdata().astype(np.uint8)


            for i in class_list:
                if np.sum(gt == i) == 0 and np.sum(prediction == i) == 0:
                    DSC_i = 1
                    NSD_i = 1
                elif np.sum(gt == i) == 0 and np.sum(prediction == i) > 0:
                    DSC_i = 0
                    NSD_i = 0
                else:
                    if i == 5 or i == 6 or i == 10:  # for Aorta, IVC, and Esophagus, only evaluate the labelled slices in ground truth
                        z_lower, z_upper = find_lower_upper_zbound(gt == i)
                        organ_i_gt, organ_i_seg = gt[:, :, z_lower:z_upper] == i, prediction[:, :, z_lower:z_upper] == i
                    else:
                        organ_i_gt, organ_i_seg = gt == i, prediction == i

                    # Check if both arrays are not empty
                    if organ_i_gt.size > 0 and organ_i_seg.size > 0:
                        surface_distances = compute_surface_distances(organ_i_gt, organ_i_seg, case_spacing)
                        DSC_i = compute_dice_coefficient(organ_i_gt, organ_i_seg)
                        NSD_i = compute_surface_dice_at_tolerance(surface_distances, label_tolerance[i])
                    else:
                        DSC_i = 0
                        NSD_i = 0

                total_dsc[i] += DSC_i
                total_nsd[i] += NSD_i
                count[i] += 1
                case_dsc[filename].append(DSC_i)
                case_nsd[filename].append(NSD_i)

    # Calculate the averages
    avg_dsc = {i: total_dsc[i] / count[i] if count[i] > 0 else 0 for i in class_list}
    avg_nsd = {i: total_nsd[i] / count[i] if count[i] > 0 else 0 for i in class_list}

    
    avg_dsc_overall = sum(total_dsc.values()) / sum(count.values())
    avg_nsd_overall = sum(total_nsd.values()) / sum(count.values())

    return avg_dsc, avg_nsd, avg_dsc_overall, avg_nsd_overall, case_dsc, case_nsd

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def store_and_print_results(prediction_file, gt_file, dice_list, all_dice, case_dice):
    print(f'Dice coefficients for {prediction_file} and {gt_file}:', dice_list)
    all_dice[prediction_file] = dice_list
    avg_dice = np.nanmean(dice_list)
    case_dice[prediction_file] = {'dice_list': dice_list, 'avg_dice': avg_dice}


def find_lower_upper_zbound(organ_mask):
    organ_mask = np.uint8(organ_mask)
    assert np.max(organ_mask) ==1, print('mask label error!')
    z_index = np.where(organ_mask>0)[2]
    z_lower = np.min(z_index)
    z_upper = np.max(z_index)
    
    return z_lower, z_upper

def save_summary(avg_dsc, avg_nsd, avg_dsc_overall, avg_nsd_overall, summary_filename, dsc_csv_filename, nsd_csv_filename, case_dsc, case_nsd, class_list):
    summary = {
        'avg_dice_by_class': avg_dsc,
        'avg_nsd_by_class': avg_nsd,
        'avg_dice_overall': avg_dsc_overall,
        'avg_nsd_overall': avg_nsd_overall,
    }

    with open(summary_filename, 'w') as f:
        json.dump(summary, f, indent=4)
        
    dsc_rows = [["Case Name"] + [f"Class_{i}" for i in class_list]]
    for case, values in case_dsc.items():
        dsc_rows.append([case] + values)

    nsd_rows = [["Case Name"] + [f"Class_{i}" for i in class_list]]
    for case, values in case_nsd.items():
        nsd_rows.append([case] + values)
        
    save_to_csv(dsc_rows, dsc_csv_filename)
    save_to_csv(nsd_rows, nsd_csv_filename)


if __name__ == "__main__":
    if not os.path.exists('summarys'):
        os.makedirs('summarys')

    prediction_folders_path = 'predict_folders_converted_to_overlap'
    prediction_folders = os.listdir(prediction_folders_path)
    gt_folder_path = 'gtsVal_overlap_label'
    
    for prediction_folder in prediction_folders:
        if os.path.exists(os.path.join('summarys', prediction_folder+'_summary.json')):
            continue
        
        start_index = prediction_folder.index('_2_') + len('_2_')
        gt_folder = os.path.join(gt_folder_path, prediction_folder[start_index:]+'_gt')
        class_list = [1, 2, 3, 4, 5, 6, 7, 8]
        
        avg_dsc, avg_nsd, avg_dsc_overall, avg_nsd_overall, case_dsc, case_nsd = process_results(os.path.join(prediction_folders_path, prediction_folder), gt_folder, class_list)
        
        summary_filename = os.path.join('summarys', f"{prediction_folder}_summary.json")
        dsc_csv_filename = os.path.join('summarys', f"{prediction_folder}_dsc.csv")
        nsd_csv_filename = os.path.join('summarys', f"{prediction_folder}_nsd.csv")
        
        save_summary(avg_dsc, avg_nsd, avg_dsc_overall, avg_nsd_overall, summary_filename, dsc_csv_filename, nsd_csv_filename, case_dsc, case_nsd, class_list)