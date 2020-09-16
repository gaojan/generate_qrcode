import os
from os import listdir
from PIL import Image, ImageDraw, ImageFont

# 参考参数48  30
font = ImageFont.truetype(os.getcwd() + os.sep + "font" + os.sep + "SourceHanSansCN-Bold_0.otf", 48, index=0)
base_dir = os.getcwd() + os.sep


def merge_image(in_img, out_img, text=None):

    toImage = Image.open(base_dir + "background_alipay.png")
    tmp_img = Image.open(in_img)

    # 裁剪图片 裁剪图片大小（左，上，右，下）
    # tmp_img = tmp_img.crop((17, 17, 570, 570))
    # print("裁剪后图片大小：", tmp_img.size)

    # 调整图片大小 参考参数 (570, 570)400, 400
    tmp_img = tmp_img.resize((625, 625), Image.ANTIALIAS)
    # print(tmp_img.size)

    # 粘贴合并图片 调节图片位置 坐标O（x, y）参考参数 (310, 360)468, 68
    toImage.paste(tmp_img, (925, 1460))

    # 添加文字
    rgba_image = toImage.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, )  # 默认黑色(255, 255, 255, 0)表示透明
    image_draw = ImageDraw.Draw(text_overlay)
    # text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # text_xy = ((rgba_image.size[0] - text_size_x) / 2, (rgba_image.size[1] - text_size_y*(-29)) / 2)

    # 调节字体位置 坐标(X, Y) 参数参数(485, 990)580, 500
    if text:
        text_xy = (480, 985)
        image_draw.text(text_xy, text, font=font, fill=(0, 0, 0, 255))  # 参考参数(0, 0, 0, 255)(255, 255, 255)
    image_after = Image.alpha_composite(rgba_image, text_overlay)
    # image_after.show()
    image_after.save(out_img)


if __name__ == '__main__':
    date = "20200825"
    filePath = base_dir + "qrcode_img" + os.sep + "alipay_qrcode_" + date
    for fn in listdir(filePath):
        im = filePath + os.sep + fn
        # textStr = fn.split(".")[0]
        om_dir = base_dir + "out_image" + os.sep + "alipay_qrcode" + os.sep
        om = om_dir + fn
        if not os.path.exists(om_dir):
            os.makedirs(om_dir)
        merge_image(im, om)
    print("merge image over!")
