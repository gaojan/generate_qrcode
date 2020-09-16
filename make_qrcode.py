#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Author: Jan Gao
# Date: 2018/8/10
# Description:
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved
"""
import os
import qrcode
import cv2
import pandas as pd
from merge_img_ybs import merge_image
from os import listdir
from urllib.request import urlretrieve
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype(os.getcwd() + os.sep + 'SOURCEHANSANSCN-REGULAR_0.OTF', 55, index=0)


def read_excel(file_path):
    data = pd.read_excel(file_path)
    return data


def read_csv(file_path):
    data = pd.read_csv(file_path, encoding='gbk')
    return data


def make_qrcode(data, save_dir):
    """生成二维码"""
    file_list = []
    for i, url in enumerate(data[u'qrcode']):
        name = str(data['qid'][i])+'.png'
        # border=5
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=40, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        try:
            img.save(save_dir + name)
            file_list.append(save_dir + name)
        except Exception as e:
            print(e)
    return file_list


def alipay_qrcode(data, save_dir):
    file_list = []
    for url in data.qrcode_url:
        name = url.split("?")[1].split("&")[0].split("=")[1] + ".png"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        try:
            img = urlretrieve(url, filename=save_dir + name)[0]
            file_list.append(img)
        except Exception as e:
            print(e)
    return file_list


def add_text_to_image(image, text, font=font):
    """添加文字到图片"""
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size,)   # 默认黑色(255, 255, 255, 0)表示透明
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)

    # 设置文本文字位置
    # text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)  #底部右下脚
    # text_xy = ((rgba_image.size[0] - text_size_x) / 2, (rgba_image.size[1] - text_size_y) / 2)  # 中间
    text_xy = ((rgba_image.size[0] - text_size_x) / 2, (rgba_image.size[1] - text_size_y*(-29)) / 2)  # 底部正中间
    # 设置文本颜色和透明度
    # image_draw.text(text_xy, text, font=font, fill=(76, 234, 124, 180))
    image_draw.text(text_xy, text, font=font, fill=(0, 0, 0, 225))
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    return image_with_text


if __name__ == '__main__':
    date = "20200825"
    filename = "alipay_qrcode_%s.csv" % date
    base_dir = os.getcwd() + os.sep
    save_dir = base_dir + os.sep + "qrcode_img" + os.sep + filename.split(".")[0] + os.sep
    filePath = base_dir + os.sep + "qrcode_data" + os.sep + filename
    suffix = filePath.split(".")[1]
    if suffix == ("xls" or "xlsx"):
        df = read_excel(filePath)
    else:
        df = read_csv(filePath)

    # 1、url生成二维码
    file_list = make_qrcode(df, save_dir)
    # 2、支付宝二维码
    alipay_qrcode(df, save_dir)

