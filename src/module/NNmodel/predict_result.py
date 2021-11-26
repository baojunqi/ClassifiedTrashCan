'''
Author       : AyanamaiYui
Date         : 2021-11-09 11:56:45
LastEditTime : 2021-11-13 11:20:02
Version      : 
Description  : 
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
from PIL import Image
import numpy as np
import os
import time
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model


# 根据预测结果显示对应的文字label
classes_types = ['0-other garbage-fast food box', '1-other garbage-soiled plastic', '2-other garbage-cigarette', '3-other garbage-toothpick', '4-other garbage-flowerpot', '5-other garbage-bamboo chopsticks', '6-kitchen waste-meal', '7-kitchen waste-bone', '8-kitchen waste-fruit peel', '9-kitchen waste-pulp', '10-kitchen waste-tea', '11-kitchen waste-Vegetable', '12-kitchen waste-eggshell', '13-kitchen waste-fish bone', '14-recyclables-powerbank', '15-recyclables-bag', '16-recyclables-cosmetic bottles', '17-recyclables-toys', '18-recyclables-plastic bowl', '19-recyclables-plastic hanger', '20-recyclables-paper bags', '21-recyclables-plug wire', '22-recyclables-old clothes', '23-recyclables-can', '24-recyclables-pillow', '25-recyclables-plush toys', '26-recyclables-shampoo bottle', '27-recyclables-glass cup', '28-recyclables-shoes', '29-recyclables-anvil', '30-recyclables-cardboard', '31-recyclables-seasoning bottle', '32-recyclables-bottle', '33-recyclables-metal food cans', '34-recyclables-pot', '35-recyclables-edible oil barrel', '36-recyclables-drink bottle', '37-hazardous waste-dry battery', '38-hazardous waste-ointment', '39-hazardous waste-expired drugs']

def generate_result(result):
    for i in range(4):
        # print(result[0])
        # print(type(result[0][i]))
        max = np.max(result[0])
        print(max)
        if(result[0][i] == max):
            print(result[0][i])
            return classes_types[i]


def show(img_path, results):
    # 对结果进行显示
    frame = cv2.imread(img_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, generate_result(results), (10, 140), font, 3, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('img', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def prepare_image(img_path, model):
    # 加载图像
    image = Image.open(img_path)
    if image.mode == 'P':
        image = image.convert('RGB')
    image = image.resize((512, 384), Image.ANTIALIAS)
    
    new_dir = os.path.join('/home/pi/workspace/IOTFinalProject/image/resized/')
    new_path = new_dir + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + ".jpg"
    image.save(new_path)
    img = load_img((new_path), target_size=(512, 384))       # x = np.array(img, dtype='float32')test
    # 图像预处理
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    results = model.predict(x)
    print(results)
    return results, new_path



def detect(img_path):
    model = load_model("/home/pi/workspace/IOTFinalProject/src/module/best_model_15_00_1.h5")
    model.compile(optimizer='Adam',
            loss='categorical_crossentropy',
            metrics=[tf.keras.metrics.categorical_accuracy])
    results, new_path = prepare_image(img_path=img_path, model=model)
    show(img_path=new_path, results=results)
    return results