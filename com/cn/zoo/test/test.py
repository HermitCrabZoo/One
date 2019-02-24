import os
import sys
import time


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


def printFlush():
    print("显示百分比")
    for x in range(101):
        mystr = "\r百分比" + str(x) + "%"
        print(mystr, end="")
        # print(mystr, end="")

        # print("\b" * (len(mystr) * 2), end="", flush=True)
        # print("\b", end="", flush=True)

        time.sleep(0.5)


def progressBar1():
    import time
    import logging
    import progressbar
    progressbar.streams.wrap_stderr()
    logging.basicConfig()

    for i in progressbar.progressbar(range(10)):
        logging.error('Got %d', i)
        time.sleep(0.2)


def progressBar2():
    import time
    import progressbar

    with progressbar.ProgressBar(max_value=10) as bar:
        for i in range(10):
            time.sleep(0.1)
            bar.update(i)


def progressBar3():
    import time
    import progressbar

    for i in progressbar.progressbar(range(100), redirect_stdout=True):
        print('Some text', i)
        time.sleep(0.1)


def progressBar4():
    import time
    import progressbar

    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    for i in range(20):
        time.sleep(0.1)
        bar.update(i)


def progressBar5():
    import time
    import progressbar

    widgets = [
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]
    for i in progressbar.progressbar(range(20), widgets=widgets):
        time.sleep(0.1)


def progressBar6():
    import time
    import progressbar

    def custom_len(value):
        # These characters take up more space
        characters = {
            '进': 2,
            '度': 2,
        }

        total = 0
        for c in value:
            total += characters.get(c, 1)

        return total

    bar = progressbar.ProgressBar(
        widgets=[
            '进度: ',
            progressbar.Bar(),
            ' ',
            progressbar.Counter(format='%(value)02d/%(max_value)d'),
        ],
        len_func=custom_len,
    )
    for i in bar(range(10)):
        time.sleep(0.2)


def progressBar7():
    import sys
    import time
    for i in range(10):
        sys.stdout.write("\r{}".format(i))
        sys.stdout.flush()
        time.sleep(0.3)


if __name__ == "__main__":
    pass
    # testSeekInWrite()
    # testSeekInRead()
    # rename(r"F:\学习\深入理解Java虚拟机（jvm性能调优+内存模型+虚拟机原理）")
    # printFlush()
    # progressBar1()
    # progressBar2()
    # progressBar3()
    # progressBar4()
    # progressBar5()
    # progressBar6()
    progressBar7()
