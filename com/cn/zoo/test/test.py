import os
import sys


def testSeekInWrite():
    # 写文件时，删掉最后一个换行符
    with open("runoob.txt", "w+", encoding="utf-8") as fo:
        fo.write("我是谁？我在哪？我为了谁？我要干什么？\n")
        fo.seek(fo.tell()-2,os.SEEK_SET)
        fo.truncate()

def testSeekInRead():
    with open("runoob.txt", "rb+") as fo:
        # fo.write(b"我是谁？我在哪？我为了谁？我要干什么？\n")
        fo.seek(-2, os.SEEK_END)
        print(fo.tell())
        print(fo.read())
        print("\n".encode("utf-8"))
        print(str("\x9f"))
        if fo.read() == "\n".encode("utf-8"):
            print("true")
            fo.seek(-1, os.SEEK_END)
            fo.truncate()


def rename(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp4") or file.endswith(".avi"):
                src = os.path.join(root, file)
                dst = os.path.join(root, file.lstrip("更多视频关注微信公众号【八戒程序猿】"))
                if src != dst:
                    os.rename(src, dst)
                    count +=1
                    print("{} -> {}".format(src, dst))
    print("total：{}".format(count))


if __name__ == "__main__":
    pass
    # testSeekInWrite()
    # testSeekInRead()
    # rename(r"F:\学习\深入理解Java虚拟机（jvm性能调优+内存模型+虚拟机原理）")
