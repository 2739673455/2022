# Pixiv搜索界面
import os
import re
import sys
import time
import random
import urllib
import urllib3
import requests
import concurrent.futures
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Thumbnail_Download_Thread(QThread):
    numsig = pyqtSignal(int)
    img_download_url = pyqtSignal(str)
    textsig = pyqtSignal(str)

    def __init__(self, thumbnail_urls):
        super().__init__()
        self.thumbnail_urls = thumbnail_urls
        self.num = 0

    def thumbnail_download(self, thumbnail_url):
        id = thumbnail_url.split('/')[-1].split('_')[0]  # 获取图片id
        file = path_t + id + '.jpg'  # 拼接文件路径
        img_url = 'https://www.pixiv.net/artworks/' + id
        resp = requests.get(img_url, headers=headers)
        viewcount = re.search('"viewCount":(.*?),', resp.text).group(1)
        self.num += 1
        self.numsig.emit(int(self.num))
        if int(viewcount) > view:
            img_download_url = re.search('"original":"(.+?)"', resp.text).group(1)
            if os.path.isfile(file) == True:
                self.textsig.emit(f'{id}已存在,{viewcount}')
            else:
                thumbnail_src = requests.get(thumbnail_url, headers=headers)
                with open(file, 'wb') as f:
                    f.write(thumbnail_src.content)
                self.textsig.emit(f'{id}已下载,{viewcount}')
            self.img_download_url.emit(str(img_download_url))
            time.sleep(random.random() + 1)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.thumbnail_download, url) for url in self.thumbnail_urls]


class Image_Download_Thread(QThread):
    textsig = pyqtSignal(str)

    def __init__(self, img_download_url):
        super().__init__()
        self.url = img_download_url
        self.id = img_download_url.split('/')[-1].split('_')[0]

    def run(self):
        file = path_i + self.id + '.jpg'
        if os.path.isfile(file) == True:
            self.textsig.emit(f'{self.id}已存在{path_i}')
        else:
            headers['referer'] = self.url
            s = requests.get(self.url, headers=headers, verify=False)
            with open(file, 'wb') as f:
                f.write(s.content)
            self.textsig.emit(f'{self.id}下载至{path_i}')


class Pixiv(QDialog):
    def __init__(self):
        super().__init__()
        self.img_d_url_dict = dict()
        self.button_num = 0
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Pixiv_搜索")
        self.resize(1600, 1200)
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QVBoxLayout()
        self.label1 = QLabel('搜索内容')
        self.label2 = QLabel('最低浏览量')
        self.label3 = QLabel('页码')
        self.lineedit1 = QLineEdit(target)
        self.lineedit2 = QLineEdit(str(view))
        self.spinbox1 = QSpinBox()
        self.spinbox1.setValue(page)
        self.scrollarea = QScrollArea(self)
        self.win = QWidget()
        self.grid = QGridLayout()
        self.textbrowser1 = QTextBrowser()
        self.textbrowser1.setFixedSize(1000, 200)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(300, 30)
        self.button2 = QPushButton('搜索')
        self.button2.setFixedSize(150, 50)
        self.button2.clicked.connect(self.start)
        self.button3 = QPushButton('清空')
        self.button3.setFixedSize(150, 50)
        self.button3.clicked.connect(self.clear)
        self.win.setLayout(self.grid)
        self.scrollarea.setWidget(self.win)
        self.layout1.addLayout(self.layout2)
        self.layout1.addWidget(self.scrollarea)
        self.layout1.addLayout(self.layout3)
        self.layout2.addWidget(self.label1)
        self.layout2.addWidget(self.lineedit1)
        self.layout2.addWidget(self.label2)
        self.layout2.addWidget(self.lineedit2)
        self.layout2.addWidget(self.label3)
        self.layout2.addWidget(self.spinbox1)
        self.layout3.addWidget(self.textbrowser1)
        self.layout3.addLayout(self.layout4)
        self.layout4.addWidget(self.progress_bar)
        self.layout4.addWidget(self.button2)
        self.layout4.addWidget(self.button3)
        self.layout4.setAlignment(self.progress_bar, Qt.AlignCenter)
        self.layout4.setAlignment(self.button2, Qt.AlignCenter)
        self.layout4.setAlignment(self.button3, Qt.AlignCenter)
        self.setLayout(self.layout1)

    def start(self):
        global target, target_encoded, view, page, path_t, path_i
        self.scrollarea.setWidgetResizable(True)
        target = self.lineedit1.text()
        target_encoded = urllib.parse.quote(target)
        view = int(self.lineedit2.text())
        page = self.spinbox1.value()
        path_t = 'D:/Pixiv_picture/' + target + '/thumbnail/'
        path_i = 'D:/Pixiv_picture/' + target + '/'
        if os.path.isdir(path_t) == False:
            os.makedirs(path_t)
        if os.path.isdir(path_i) == False:
            os.mkdir(path_i)
        self.thumbnail_urls = self.get_url(headers, page)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self.thumbnail_urls))
        self.thumbnail_download_thread = Thumbnail_Download_Thread(self.thumbnail_urls)
        self.thumbnail_download_thread.numsig.connect(self.refresh_progress_bar)
        self.thumbnail_download_thread.img_download_url.connect(self.addimgbutton)
        self.thumbnail_download_thread.textsig.connect(self.append_text)
        self.thumbnail_download_thread.start()

    def get_url(self, headers, page):  # 获取搜索页缩略图的url,返回url列表
        url = f'https://www.pixiv.net/ajax/search/artworks/{target_encoded}'
        headers['referer'] = url
        resp = requests.get(url, headers=headers, verify=False)
        thumbnail_urls = re.findall(',"url":"(.*?)",', resp.text)
        thumbnail_urls = [thumbnail_urls[i].replace('\\', '') for i in range(len(thumbnail_urls))]
        return thumbnail_urls

    def addimgbutton(self, img_download_url):
        id = img_download_url.split('/')[-1].split('_')[0]
        thumbnail = path_t + id
        self.button1 = QPushButton()
        self.button1.setIcon(QIcon(thumbnail))
        self.button1.setIconSize(QSize(250, 250))
        self.img_d_url_dict[thumbnail] = img_download_url
        self.button1.clicked.connect(lambda: self.img_download(self.img_d_url_dict[thumbnail]))
        self.grid.addWidget(self.button1, self.button_num // 5, self.button_num % 5)
        self.win.resize(1500, 250 * (self.button_num // 5 + 1))
        self.button_num += 1

    def img_download(self, img_download_url):
        self.image_download_thread = Image_Download_Thread(img_download_url)
        self.image_download_thread.textsig.connect(self.append_text)
        self.image_download_thread.start()

    def append_text(self, text):
        self.textbrowser1.append(text)

    def refresh_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def clear(self):
        self.button_num = 0
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    urllib3.disable_warnings()
    target = '原神'
    target_encoded = urllib.parse.quote(target)
    view = 100
    page = 1
    path_t = 'D:/Pixiv_picture/' + target + '/thumbnail/'
    path_i = 'D:/Pixiv_picture/' + target + '/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',

        'Cookie': 'first_visit_datetime_pc=2023-03-22+23%3A46%3A27; p_ab_id=7; p_ab_id_2=7; p_ab_d_id=268037037; yuid_b=JSeGdIU; privacy_policy_notification=0; a_type=1; b_type=1; login_ever=yes; c_type=25; _fbp=fb.1.1691290932968.366527084; privacy_policy_agreement=6; __utmz=235335808.1694517025.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __cf_bm=hks_l_xU_LWD.0JYrWFCoioS_HzhgnzALqS._48M_mM-1695515414-0-ARxcdhHYeSL3WvYIU2S/u1m0nGflARcaKxQx/2huelNaMK51js8RC8OYg3Et0+QHHQTvUVWxCTeSo4ntDB//mJNit9TOOw5aQHIdf0nLfArr; __utma=235335808.811011881.1679496389.1694517025.1695515428.2; __utmc=235335808; __utmt=1; _gid=GA1.2.637506940.1695515431; _gcl_au=1.1.316082557.1695515437; PHPSESSID=92669508_Tns1ccTgBT2mHTmXIDhrIv9kqm5qDaJm; device_token=39aacf357b82306419530e5e78137e4a; _ga_MZ1NL4PHH0=GS1.1.1695515439.6.0.1695515443.0.0.0; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=92669508=1^9=p_ab_id=7=1^10=p_ab_id_2=7=1^11=lang=zh=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _im_vid=01HB29H4SJ2S5AV2CT1Y44N823; cf_clearance=e_ifxOXYqx0G_SrTHlXVB8lwa4N7Iun23k.hZZSBG0Y-1695515458-0-1-550efdb.f64f8a9.5251b03b-0.2.1695515458; user_language=zh; cto_bundle=pIho1V9XYWRFNGROOHVBSUdUaXFjT1g1ZzFRRmZuQzVKSWVRMmIyRk9GVzNRU2ExV09DbGtMN2U2RktBMWQzcWR1T3FMSGdaM1VWZGlkTUtKQkNnTkRqYTBFTXlMTHF5YnNGaGZ3OTBWWVNoa3JoaXlNeDRIOHlyV1gyQ3RTN2hLUXVzWHUwbGRmN3R0c3JKOFFMRExseEd0aVElM0QlM0Q; _ga=GA1.2.811011881.1679496389; _gat_UA-1830249-3=1; __utmb=235335808.8.10.1695515428; _ga_75BBYNYN9J=GS1.1.1695515428.15.1.1695515515.0.0.0',
    }
    app = QApplication(sys.argv)
    w = Pixiv()
    w.show()
    app.exec()
