from comm import *
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim.nets as nets
import os


def threshold_image(filepath):
    """使用PIL的方式二值化图片，返回ndarray对象"""
    image = Image.open(filepath)
    image = image.convert("L")
    arr = np.array(image)
    arr = (arr > 130) * 255
    return arr


def threshold(filepath):
    """使用cv2的方式二值化图片，返回ndarray对象"""
    image = filepath if isinstance(filepath, np.ndarray) else cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    v, arr = cv2.threshold(image, 130, 255, 0)
    return arr


def vec2name(vec):
    """向量转成标签名字"""
    return "".join([chr(i + 97) for i in vec])


def crop(ndarray):
    """
    Takes cv2 image, im, and padding % as a float, padding,
    and returns cropped image.
    """
    # 450*114
    w, h, padding = 500, 126, 10
    tow_dim = ndarray[padding:-padding, padding:-padding, 0]
    rows, cols = tow_dim.shape
    coord_sum = []
    for r in range(rows-h+1):
        for c in range(cols-w+1):
            coord_sum.append([r, c, tow_dim[r:r+h, c:c+w].sum()])
    result = np.array(coord_sum)
    v = result[:, 2]
    r, c, s = result[np.where(v == np.min(v))[0].min(), :]
    cropped = ndarray[r+padding:r+padding+h, c+padding:c+padding+w, :]
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
        for i, pic in enumerate(os.listdir(test_dir)):
            # if i >= 1:
            #     break
            pic_path = os.path.join(test_dir, pic)
            threshold_img = threshold(pic_path)
            # manual = threshold_img[36:150, 165:615]
            # 裁剪
            cropped = crop(threshold_img)
            # Image.fromarray(croped).convert('RGB').show()
            arr = cv2.resize(cropped, (224, 224))
            img2 = tf.reshape(arr.astype('uint8'), [1, 224, 224, 3])
            img3 = tf.cast(img2, tf.float32) / 255.0

            name = os.path.splitext(pic)[0]

            b_image = session.run(img3)
            t_label = session.run(max_idx_p, feed_dict={x: b_image})
            vec = t_label[0].tolist()
            predict_text = vec2name(vec)
            print('真实值：{}   预测值：{}'.format(name, predict_text))
            Image.fromarray(cropped).save(os.path.join(r"E:\result\recog", "{}.jpg".format(predict_text)))


if __name__ == "__main__":
    # do_predict()
    f = r"E:\result\img\ali2011_21862650_5c885e45a9a11.jpg"
    image = cv2.imread(f)
    th = threshold(cv2.bilateralFilter(src=image, d=3, sigmaColor=140, sigmaSpace=140))
    # Image.fromarray(th).show()
    # dst = cv2.medianBlur(th, 3)
    # dst = cv2.GaussianBlur(th, (3, 3), 0)
    dst = threshold(cv2.bilateralFilter(src=image, d=1, sigmaColor=100, sigmaSpace=100))
    line = np.zeros((1, 800, 3), dtype='uint8')
    print(line.shape)
    Image.fromarray(np.vstack((th, line, dst))).show()


