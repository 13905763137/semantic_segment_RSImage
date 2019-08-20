# coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential,load_model
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization, Reshape, Permute, Activation, Input
from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import img_to_array
from keras.callbacks import ModelCheckpoint, EarlyStopping, History,ReduceLROnPlateau
from keras.models import Model
from keras.layers.merge import concatenate
from keras.utils import plot_model
import matplotlib.pyplot as plt
import cv2
import random
import sys
import os
import time
from tqdm import tqdm
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.models import load_model

from keras import backend as K
K.set_image_dim_ordering('tf')
from keras.callbacks import TensorBoard
from keras.utils import multi_gpu_model

from ulitities.base_functions import load_img_normalization, load_img_normalization_bybandlist, load_img_by_gdal, UINT16, UINT8, UINT10

seed = 4
np.random.seed(seed)
from keras import metrics, losses
from keras.losses import binary_crossentropy
from segmentation_models.losses import *
from segmentation_models.metrics import iou_score
from segmentation_models.losses import self_define_loss, bce, cce

from segmentation_models import Unet,FPN,PSPNet,Linknet
from segmentation_models.deeplab.model import Deeplabv3

from utils import save, update_config
from config import Config
import json
import sys
# from crfrnn.crfrnn_model import get_crfrnn_model_def
from crfrnn.crfrnn_layer import CrfRnnLayer
import crfrnn.util

import  argparse
parser=argparse.ArgumentParser(description='RS classification train')
parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]', nargs='+',
                        default=1, type=int)
parser.add_argument('--config', dest='config_file', help='json file to config',
                         default='config_scrs_bieshu.json')
args=parser.parse_args()
gpu_id=args.gpu_id
print("gpu_id:{}".format(gpu_id))
# os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
if isinstance(gpu_id,int):
    os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)
elif isinstance(gpu_id,list):
    tp_str =[]
    for i in gpu_id:
        tp_str.append(str(i))
    ns = ",".join(tp_str)
    os.environ["CUDA_VISIBLE_DEVICES"] = ns
else:
    pass

with open(args.config_file, 'r') as f:
    cfg = json.load(f)

config = Config(**cfg)
print(config)

FLAG_MAKE_TEST=True
im_type=UINT8
if '10' in config.im_type:
    im_type=UINT10
elif '16' in config.im_type:
    im_type=UINT16
else:
    pass

date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
print("date and time: {}".format(date_time))
print("traindata from: {}".format(config.train_data_path))
band_name=''
if len(config.band_list)==0:
    band_name='fullbands'
else:
    for i in range(len(config.band_list)):
         band_name +=str(config.band_list[i])
    band_name+="bands"
print("band_name:{}".format(band_name))
if not os.path.isdir(config.model_dir):
    print("Warning: model saveing directory is empty!")
    os.mkdir(config.model_dir)
model_save_path = ''.join([config.model_dir,'/',config.target_name, '_', config.network, '_',config.BACKBONE,'_',config.loss,'_',config.optimizer,'_',str(config.img_w), '_',band_name,'_', date_time, 'best.h5'])
print("model save as to: {}".format(model_save_path))
last_model = ''.join([config.model_dir,'/',config.target_name, '_', config.network, '_',config.BACKBONE,'_',config.loss,'_',config.optimizer,'_',str(config.img_w), '_',band_name,'_', date_time, 'last.h5'])

"""get the train file name and divide to train and val parts"""
def get_train_val(val_rate=config.val_rate):
    train_url = []
    train_set = []
    val_set = []
    for pic in os.listdir(config.train_data_path + '/train/label'):
        train_url.append(pic)
    random.shuffle(train_url)
    total_num = len(train_url)
    val_num = int(val_rate * total_num)
    for i in range(len(train_url)):
        if i < val_num:
            val_set.append(train_url[i])
        else:
            train_set.append(train_url[i])
    return train_set, val_set


# data for training
def generateData(config, data=[]):
    # print 'generateData...'
    while True:
        train_data = []
        train_label = []
        batch = 0
        for i in (range(len(data))):
            url = data[i]
            batch += 1

            try:
                _, img = load_img_normalization_bybandlist((config.train_data_path + '/train/src/' + url), bandlist=config.band_list, data_type=im_type)
            except RuntimeError:
                raise RuntimeError("Open file faild:{}".format(url))

            # Adapt dim_ordering automatically
            img = img_to_array(img)
            train_data.append(img)
            _, label = load_img_normalization(1, (config.train_data_path + '/train/label/' + url))
            label = img_to_array(label)
            train_label.append(label)
            if batch % config.batch_size == 0:
                # print 'get enough bacth!\n'
                train_data = np.array(train_data)
                train_label = np.array(train_label)
                if config.nb_classes>2:
                    train_label = to_categorical(train_label, num_classes=config.nb_classes)
                # train_label = train_label.reshape((config.batch_size, config.img_w * config.img_h,config.nb_classes))
                # print("train_label shape:{}".format(train_label.shape))

                yield (train_data, train_label)
                train_data = []
                train_label = []
                batch = 0


# data for validation
def generateValidData(config, data=[]):
    # print 'generateValidData...'
    while True:
        valid_data = []
        valid_label = []
        batch = 0
        for i in (range(len(data))):
            url = data[i]
            batch += 1
            try:
                _, img = load_img_normalization_bybandlist((config.train_data_path + '/train/src/' + url), bandlist=config.band_list,data_type=im_type)
            except RuntimeError:
                raise RuntimeError("Open file faild:{}".format(url))
            # Adapt dim_ordering automatically
            img = img_to_array(img)
            valid_data.append(img)
            _, label = load_img_normalization(1, (config.train_data_path + '/train/label/' + url))
            label = img_to_array(label)
            valid_label.append(label)
            if batch % config.batch_size == 0:
                valid_data = np.array(valid_data)
                valid_label = np.array(valid_label)
                if config.nb_classes>2:
                    valid_label = to_categorical(valid_label, num_classes=config.nb_classes)
                # valid_label = valid_label.reshape((config.batch_size, config.img_w * config.img_h,config.nb_classes))
                yield (valid_data, valid_label)
                valid_data = []
                valid_label = []
                batch = 0

def transfer_weights(trained_backbone, model):
    for i, layer in enumerate(trained_backbone.layers):
        weights = layer.get_weights()
        model.layers[i].set_weights(weights)

"""Train model ............................................."""
def train(model):

    if os.path.isfile(config.base_model):
        try:
            model.load_weights(config.base_model)
        except ValueError:
            print("Can not load weights from base model: {}".format(config.base_model))
        else:
            print("loaded weights from base model:{}".format(config.base_model))

    model_checkpoint = ModelCheckpoint(
        model_save_path,
        monitor=config.monitor,
        save_best_only=config.save_best_only,
        mode=config.mode
    )

    model_earlystop = EarlyStopping(
        monitor=config.monitor,
        patience=config.patience+5,
        verbose=0,
        mode=config.mode
    )

    # """自动调整学习率"""
    model_reduceLR=ReduceLROnPlateau(
        monitor=config.monitor,
        factor=config.factor,
        patience=config.patience,
        verbose=0,
        mode=config.mode,
        epsilon=config.epsilon,
        cooldown=config.cooldown,
        min_lr=config.min_lr
    )

    model_history = History()

    logdir = ''.join([config.log_dir,'/log',config.target_name,"_", config.network,"_",config.BACKBONE,"_", config.loss, date_time])
    if not os.path.isdir(logdir):
        print("Warning: ")
        os.mkdir(logdir)

    tb_log = TensorBoard(log_dir=logdir)

    callable = [model_checkpoint,model_earlystop, model_reduceLR, model_history, tb_log]
    # callable = [model_checkpoint, model_reduceLR, model_history, tb_log]
    # callable = [model_checkpoint]

    train_set, val_set = get_train_val()
    train_numb = len(train_set)
    valid_numb = len(val_set)
    print ("the number of train data is", train_numb)
    print ("the number of val data is", valid_numb)

    if isinstance(gpu_id,int):
        print("using single gpu {}".format(gpu_id))
        pass
    elif isinstance(gpu_id,list):
        print("using multi gpu {}".format(gpu_id))
        if len(gpu_id)>1:
            model = multi_gpu_model(model, gpus=len(gpu_id))

    self_optimizer = SGD(lr=config.lr, decay=1e-6, momentum=0.99, nesterov=True)
    if 'adagrad' in config.optimizer:
        self_optimizer = Adagrad(lr=config.lr, decay=1e-6)
    elif 'adam' in config.optimizer:
        self_optimizer = Adam(lr=config.lr, decay=1e-6)
    else:
        pass


    try:
        model.compile(self_optimizer, loss=self_define_loss(config.loss, config.class_weights), metrics=[config.metrics])
        H = model.fit_generator(generator=generateData(config, train_set),
                            steps_per_epoch=train_numb // config.batch_size,
                            epochs=config.epochs,
                            verbose=1,
                            validation_data=generateValidData(config, val_set),
                            validation_steps=valid_numb // config.batch_size,
                            callbacks=callable,
                            max_q_size=1)
    except:
        print("Warning: compile failed with customer loss function and class_weights")
        print("Now, using default loss function without class_weights...")
        model.compile(self_optimizer, loss=config.loss, metrics=[config.metrics])
        H = model.fit_generator(generator=generateData(config, train_set),
                                steps_per_epoch=train_numb // config.batch_size,
                                epochs=config.epochs,
                                verbose=1,
                                validation_data=generateValidData(config, val_set),
                                validation_steps=valid_numb // config.batch_size,
                                callbacks=callable,
                                max_q_size=1,
                                class_weight='auto')
    finally:
        print("Compile model successfully!")


    model.save(last_model)
"""
Test the model which has been trained right now
"""
window_size=config.img_w
def test_predict(bands, image,model):
    stride = window_size

    h, w, _ = image.shape
    print('h,w:', h, w)
    padding_h = (h // stride + 1) * stride
    padding_w = (w // stride + 1) * stride
    padding_img = np.zeros((padding_h, padding_w, bands))
    padding_img[0:h, 0:w, :] = image[:, :, :]

    padding_img = img_to_array(padding_img)

    mask_whole = np.zeros((padding_h, padding_w), dtype=np.float32)
    for i in list(range(padding_h // stride)):
        for j in list(range(padding_w // stride)):
            crop = padding_img[i * stride:i * stride + window_size, j * stride:j * stride + window_size, :bands]

            crop = np.expand_dims(crop, axis=0)
            print('crop:{}'.format(crop.shape))

            pred = model.predict(crop, verbose=2)
            # pred = np.argmax(pred, axis=2)  #for one hot encoding
            pred[pred < 0.5] = 0
            pred[pred >= 0.5] = 1

            pred = pred.reshape(256, 256)
            print(np.unique(pred))

            mask_whole[i * stride:i * stride + window_size, j * stride:j * stride + window_size] = pred[:, :]

    outputresult =mask_whole[0:h,0:w]
    # outputresult = outputresult.astype(np.uint8)

    plt.imshow(outputresult, cmap='gray')
    plt.title("Original predicted result")
    plt.show()
    cv2.imwrite('../../data/predict/test_model_new.png',outputresult*255)
    return outputresult

def add_new_model(base_moldel, cofig):
    x = base_moldel.get_layer('softmax').output
    x = Reshape((config.img_w * config.img_h,config.nb_classes))(x)
    model=Model(input=base_moldel.input, output=x)
    return model
def add_crfrnn(base_model, cofig):
    img_input = base_model.input
    # x = base_model.get_layer('final_conv').output
    x = base_model.output
    x = CrfRnnLayer(image_dims=(config.img_w, config.img_h),
                         num_classes=config.nb_classes,
                         theta_alpha=160.,
                         theta_beta=3.,
                         theta_gamma=3.,
                         num_iterations=5,
                         name='crfrnn')([x, img_input])

    # x = Activation(config.activation, name=config.activation)(x)
    model = Model(img_input, x)
    model.summary()
    return model


def test(model_file,config):
    test_data_path=os.path.join(config.train_data_path + 'test')
    if not os.path.isdir(test_data_path):
        print("test data path is not exist!")
        return -1
    test_url=[]
    for pic in os.listdir(test_data_path + '/label'):
        test_url.append(pic)
    random.shuffle(test_url)
    if not os.path.isfile(model_file):
        print("Error: model file is not exist")
        return -2
    model = load_model(model_file)
    test_data = []
    test_label = []
    test_loss = []
    batch = 0
    for i in (range(len(test_url))):
        url = test_url[i]
        batch += 1
        try:
            _, img = load_img_normalization_bybandlist((test_data_path + '/src/' + url),
                                                       bandlist=config.band_list,
                                                       data_type=im_type)
        except RuntimeError:
            raise RuntimeError("Open file faild:{}".format(url))
        # Adapt dim_ordering automatically
        img = img_to_array(img)
        test_data.append(img)
        _, label = load_img_normalization(1, (test_data_path + '/label/' + url))
        label = img_to_array(label)
        test_label.append(label)
        if batch % config.batch_size == 0:
            # print 'get enough bacth!\n'
            test_data = np.array(test_data)
            test_label = np.array(test_label)
            if config.nb_classes > 2:
                test_label = to_categorical(test_label, num_classes=config.nb_classes)
            test_result = model.test_on_batch(test_data, test_label)
            print("testing ...{}:{}".format(model.metrics_names, test_result))
            test_loss.append(test_result)
            test_data = []
            test_label = []
            batch = 0
    test_loss=np.array(test_loss)
    print("test accuracy:{}".format(np.average(test_loss,axis=0)))

    # test_data = np.array(test_data)
    # test_label = np.array(test_label)
    # if config.nb_classes > 2:
    #     test_label = to_categorical(test_label, num_classes=config.nb_classes)
    # test_loss = model.evaluate(test_data, test_label, batch_size=8)
    # print("test acc: {}:{}".format(model.metrics_names, test_loss))



if __name__ == '__main__':

    if not os.path.isdir(config.train_data_path):
        print ("train data does not exist in the path:\n {}".format(config.train_data_path))
        sys.exit(-1)

    if len(config.band_list)==0:
        print("Error: band_list should not be empty!")
        sys.exit(-2)
    input_layer = (config.img_w,config.img_h, len(config.band_list))
    if 'unet' in config.network:
        model = Unet(backbone_name=config.BACKBONE, input_shape=input_layer,
                 classes=config.nb_classes, activation=config.activation,
                 encoder_weights=config.encoder_weights)
        model = add_crfrnn(model, config)
        model.summary()
        # plot_model(model, to_file='unet_crfrnn_model.png')

        # sys.exit(-1)


    elif 'pspnet' in config.network:
        model = PSPNet(backbone_name=config.BACKBONE, input_shape=input_layer,
                     classes=config.nb_classes, activation=config.activation,
                     encoder_weights=config.encoder_weights,psp_dropout=config.dropout)
    elif 'fpn' in config.network:
        model = FPN(backbone_name=config.BACKBONE, input_shape=input_layer,
                     classes=config.nb_classes, activation=config.activation,
                     encoder_weights=config.encoder_weights, pyramid_dropout=config.dropout)
    elif 'linknet' in config.network:
        model = Linknet(backbone_name=config.BACKBONE, input_shape=input_layer,
                     classes=config.nb_classes, activation=config.activation,
                     encoder_weights=config.encoder_weights)
    elif 'deeplabv3plus' in config.network:
        try:
            model = Deeplabv3(weights=config.encoder_weights, input_shape=input_layer,
                          classes=config.nb_classes, backbone=config.BACKBONE, activation=config.activation)
        except RuntimeError:
            print("Warning: Run this model with a backend that does not support separable convolutions.")
            model = Deeplabv3(weights=None, input_shape=input_layer,
                              classes=config.nb_classes, backbone="mobilenetv2", activation=config.activation)
        except ValueError:
            print("Warning:  invalid argument for `weights` or `backbone.")
            model = Deeplabv3(weights=None, input_shape=input_layer,
                              classes=config.nb_classes, backbone="mobilenetv2", activation=config.activation)
        else:
            print("input parameters correct for deeplab V3+!")
        # finally:
        #     print("deeplab model")

    else:
        print("Error:")


    print(model.summary())
    print("Train by : {}_{}".format(config.network, config.BACKBONE))
    #
    # model=add_new_model(model, config)
    # print(model.summary())

    """ Training model........"""
    train(model)

    print("[Info]:test model...")
    # model_save_path = '/media/omnisky/b1aca4b8-81b8-4751-8dee-24f70574dae9/bieshu/models/20190731/bieshu_pspnet_inceptionresnetv2_binary_crossentropy_adam_480_012bands_2019-08-01_11-24-18best.h5'
    test(model_save_path,config)





