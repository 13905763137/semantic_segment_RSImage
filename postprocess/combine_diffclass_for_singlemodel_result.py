#coding:utf-8

import os
import cv2
import numpy as np

from tqdm import tqdm
import matplotlib.pyplot as plt

from ulitities.base_functions import load_img_by_cv2

FOREGROUND = 127# for segnet:40; for unet=127; define the foreground value

ROAD_VALUE=127
BUILDING_VALUE=255

"""for unet"""
# input_path = '/media/omnisky/e0331d4a-a3ea-4c31-90ab-41f5b0ee2663/Tianfuxinqu/pred/pred_256/'
input_path = '../../data/test/tianfuxinqu/pred/pred_256/'
mask_pool = ['mask_binary_fw01_buildings_jaccard.png', 'mask_binary_fw01_roads_jaccard.png']
output_file = input_path+'/combined/mask_2018_256_fw0_smooth_combined.png'
print(output_file)

# mask_pool = ['mask_multiclass_3_buildings.png','mask_multiclass_3_roads.png']
# output_file = '../../data/predict/unet/unet_multiclass_combined_3.png'

"""for segnet"""
# input_path = '../../data/predict/segnet/'
# mask_pool = ['mask_binary_3_buildings.png','mask_binary_3_roads.png']
# output_file = '../../data/predict/segnet/segnet_binary_combined_3.png'

# mask_pool = ['mask_multiclass_3_buildings.png','mask_multiclass_3_roads.png']
# output_file = '../../data/predict/segnet/segnet_multiclass_combined_3.png'


def check_input_file(path,masks):
    ret, img_1 = load_img_by_cv2(path+masks[0], grayscale=True)
    assert (ret == 0)

    height, width = img_1.shape
    num_img = len(masks)

    for next_index in range(1,num_img):
        next_ret, next_img=load_img_by_cv2(path+masks[next_index],grayscale=True)
        assert (next_ret ==0 )
        next_height, next_width = next_img.shape
        assert(height==next_height and width==next_width)
    return height, width



def combine_all_mask(height, width,input_path,mask_pool):
    """

    :param height:
    :param width:
    :param input_path:
    :param mask_pool:
    :return: final mask from roads_mask and buildings_mask

    prior: road(1)>bulidings(2)
    """
    final_mask=np.zeros((height,width),np.uint8)
    for idx,file in enumerate(mask_pool):
        ret,img = load_img_by_cv2(input_path+file,grayscale=True)
        assert (ret == 0)
        label_value=0
        if 'road' in file:
            label_value =ROAD_VALUE
        elif 'building' in file:
            label_value=BUILDING_VALUE
        # label_value = idx+1
        # print("buildings prior")
        print("Roads prior")
        for i in tqdm(range(height)):
            for j in range(width):
                if img[i,j]>=FOREGROUND:
                    # print ("img[{},{}]:{}".format(i,j,img[i,j]))

                    if label_value == ROAD_VALUE:
                        final_mask[i, j] = label_value
                    elif label_value == BUILDING_VALUE and final_mask[i, j] != ROAD_VALUE:
                        final_mask[i, j] = label_value

                    # if label_value == BUILDING_VALUE:
                    #     final_mask[i, j] = label_value
                    # elif label_value == ROAD_VALUE and final_mask[i, j] != BUILDING_VALUE:
                    #     final_mask[i, j] = label_value

    final_mask[final_mask == ROAD_VALUE] = 1
    final_mask[final_mask == BUILDING_VALUE] = 2
    return final_mask



if __name__=='__main__':

    x,y=check_input_file(input_path,mask_pool)

    result_mask=combine_all_mask(x,y,input_path,mask_pool)

    plt.imshow(result_mask, cmap='gray')
    plt.title("combined mask")
    plt.show()

    cv2.imwrite(output_file,result_mask)
    print("Saved to : {}".format(output_file))