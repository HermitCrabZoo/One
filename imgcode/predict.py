from comm import *
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim.nets as nets
import os
import re

name_dup = re.compile(r"\w+( \(\d+\))")


def threshold_image(filepath):
    """使用PIL的方式二值化图片，返回ndarray对象"""
    image = Image.open(filepath)
    image = image.convert("L")
    arr = np.array(image)
    arr = (arr > 130) * 255
    return arr


def threshold(filepath):
    """使用cv2的方式二值化图片，返回ndarray对象，比PIL的方式更高效。"""
    image = filepath if isinstance(filepath, np.ndarray) else cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    # 双边滤波器，更好保留边缘
    image = cv2.bilateralFilter(src=image, d=1, sigmaColor=80, sigmaSpace=80)
    # 二值化，大于130的设为255
    v, image = cv2.threshold(image, 130, 255, 0)
    # 等比例缩放到161*644
    image = cv2.resize(image, (644, 161))
    return image


def vec2name(vec):
    """向量转成标签名字(预测值)"""
    return "".join([chr(i + 97) for i in vec])


def crop(ndarray):
    """
    Takes cv2 image, im, and padding % as a float, padding,
    and returns cropped image.
    """
    # 截取大小450*114
    w, h = 450, 114
    # 由于原图片可能存在字母靠边缘过于近，所以使用一个更大的矩阵来承载。
    # 二值化后3个通道的二维矩阵相同，所以只截取一个通道的二维矩阵，减少计算的数量。
    canvas = np.full(np.array(ndarray.shape[0:2])+100, 255, dtype=np.uint8)
    canvas[50:-50, 50:-50] = ndarray[:, :, 0]
    rows, cols = canvas.shape
    # 计算元素为零(黑色)的平均中心点坐标
    b_rows, b_cols = np.where(canvas == 0)
    r, c = int(b_rows.mean().round())-10, int(b_cols.mean().round())
    if rows - r < int(h/2):
        r += rows - r - int(h/2) - int(h/2)
    elif r < int(h/2):
        r -= r
    else:
        r -= int(h/2)
    if cols - c < int(w/2):
        c += cols - c - int(w/2) - int(w/2)
    elif c < int(w/2):
        c -= c
    else:
        c -= int(w/2)
    cropped = canvas[r:r + h, c:c + w]
    # 将二维矩阵还原成三维
    cropped = np.repeat(cropped, (3, )).reshape((h, w, 3))
    return cropped


def do_predict():
    model_dir = project_root_with(r'imgcode\model1\train.model-240000')
    x = tf.placeholder(tf.float32, [None, 224, 224, 3])
    pred, end_points = nets.resnet_v2.resnet_v2_50(x, num_classes=6 * 26, is_training=True)
    predict = tf.reshape(pred, [-1, 6, 26])
    max_idx_p = tf.argmax(predict, 2)
    saver = tf.train.Saver()
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        saver.restore(session, model_dir)
        test_dir = r'E:\result\img'
        correct = 0
        for i, pic in enumerate(os.listdir(test_dir)):
            # if "distal" in pic:
            #     print(pic)
            # if i >= 1:
            #     break
            threshold_img = threshold(os.path.join(test_dir, pic))
            # 裁剪
            cropped = crop(threshold_img)
            # 缩小
            resized = cv2.resize(cropped, (224, 224))
            img2 = tf.reshape(resized.astype('uint8'), [1, 224, 224, 3])
            img3 = tf.cast(img2, tf.float32) / 255.0

            b_image = session.run(img3)
            t_label = session.run(max_idx_p, feed_dict={x: b_image})
            vec = t_label[0].tolist()
            predict_text = vec2name(vec)
            name = os.path.splitext(pic)[0]
            matched = name_dup.match(name)
            if matched:
                name = name.rstrip(matched.group(1))
            print('真实值：{}   预测值：{}'.format(name, predict_text))
            if name == predict_text:
                correct += 1
            Image.fromarray(cropped).save(os.path.join(r"E:\result\recog", "{}.jpg".format(predict_text)))
        print("准确：{}  错误：{}  正确率：{}".format(correct, i-correct+1, correct / (i+1)))


if __name__ == "__main__":
    do_predict()
    # test_dir = r'E:\result\img'
    # for i, pic in enumerate(os.listdir(test_dir)):
    #     threshold_img = threshold(os.path.join(test_dir, pic))
    #     # 裁剪
    #     cropped = crop(threshold_img)
    #     # 保存为单通道图
    #     Image.fromarray(cropped).save(os.path.join(r"E:\result\img-pre", pic))
    # f = r"E:\result\img\tufoli.jpg"
    # image = cv2.imread(f)
    # th = threshold(cv2.bilateralFilter(src=image, d=3, sigmaColor=140, sigmaSpace=140))
    # Image.fromarray(th).show()
    # dst = cv2.medianBlur(th, 3)
    # dst = cv2.GaussianBlur(th, (3, 3), 0)
    # dst = threshold(cv2.bilateralFilter(src=image, d=1, sigmaColor=50, sigmaSpace=50))
    # print(image.shape)
    # print(th.shape)
    # print(dst.shape)
    # line = np.zeros((1, 800, 3), dtype='uint8')
    # Image.fromarray(np.vstack((image, line, th, line, dst))).show()


