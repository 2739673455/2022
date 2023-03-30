# Pixiv搜索界面
import os
import re
import sys
import urllib
import urllib3
import requests
import concurrent.futures
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Thumbnail_Download_Thread(QThread): #下载预览图线程
    num_sign = pyqtSignal(int)
    img_download_url = pyqtSignal(str)
    textsig = pyqtSignal(str)
    def __init__(self,thumbnail_urls):
        super().__init__()
        self.thumbnail_urls = thumbnail_urls
        self.num = 0

    def thumbnail_download(self,thumbnail_url):
        id=thumbnail_url.split('/')[-1].split('_')[0] #获取图片id
        file=path_t+id+'.jpg' #获取文件路径
        img_url = 'https://www.pixiv.net/artworks/'+id
        resp = requests.get(img_url,headers=headers)
        viewcount = re.search('"viewCount":(.*?),',resp.text).group(1)
        self.num+=1
        self.num_sign.emit(int(self.num))
        if int(viewcount)>view:
            img_download_url = re.search('"original":"(.+?)"',resp.text).group(1)
            thumbnail_=requests.get(thumbnail_url,headers=headers,proxies=proxies)
            if os.path.isfile(file)==True:
                self.textsig.emit(f'{id}已存在,{viewcount}')
            else:
                with open(file,'wb') as f:
                    f.write(thumbnail_.content)
                self.textsig.emit(f'{id}已下载,{viewcount}')
            self.img_download_url.emit(str(img_download_url))

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.thumbnail_download, url) for url in self.thumbnail_urls]

class Image_Download_Thread(QThread): #下载高清图线程
    textsig = pyqtSignal(str)
    def __init__(self,img_download_url):
        super().__init__()
        self.url = img_download_url
        self.id = img_download_url.split('/')[-1].split('_')[0]

    def run(self):
        file = path_i+self.id+'.jpg'
        if os.path.isfile(file)==True:
            self.textsig.emit(f'{self.id}已存在{path_i}')
        else:
            headers['referer']=self.url
            s = requests.get(self.url,headers=headers,verify=False,proxies=proxies)
            with open(file,'wb') as f:
                f.write(s.content)
            self.textsig.emit(f'{self.id}下载至{path_i}')
            s.close()

class Pixiv(QDialog):
    def __init__(self):
        super().__init__()
        self.img_d_url_dict = dict()
        self.button_num = 0
        self.initUI()
    
    def initUI(self):
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.setWindowTitle("Pixiv_搜索")
        self.resize(1600,1200)
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
        self.textbrowser1.setFixedSize(1000,200)
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
        global target,target1,view,page,path_t,path_i
        self.scrollarea.setWidgetResizable(True)
        target = self.lineedit1.text()
        target1 = urllib.parse.quote(target)
        view = int(self.lineedit2.text())
        page = self.spinbox1.value()
        path_t = 'D:/Pixiv_picture/'+target+'/thumbnail/'
        path_i = 'D:/Pixiv_picture/'+target+'/image/'
        if os.path.isdir(path_t)==False:
            os.makedirs(path_t)
        if os.path.isdir(path_i)==False:
            os.mkdir(path_i)
        self.thumbnail_urls = self.get_url(headers,page)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self.thumbnail_urls))
        self.thumbnail_download_thread = Thumbnail_Download_Thread(self.thumbnail_urls)
        self.thumbnail_download_thread.num_sign.connect(self.refresh_progress_bar)
        self.thumbnail_download_thread.img_download_url.connect(self.addimgbutton)
        self.thumbnail_download_thread.textsig.connect(self.append_text)
        self.thumbnail_download_thread.start()
    
    def clear(self):
        self.button_num = 0
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def addimgbutton(self,img_download_url): #添加按钮
        id = img_download_url.split('/')[-1].split('_')[0]
        thumbnail = path_t+id
        self.button1 = QPushButton()
        self.button1.setIcon(QIcon(thumbnail))
        self.button1.setIconSize(QSize(250,250))
        self.img_d_url_dict[thumbnail] = img_download_url
        self.button1.clicked.connect(lambda x=thumbnail:self.img_download(self.img_d_url_dict[thumbnail]))
        self.grid.addWidget(self.button1,self.button_num//5,self.button_num%5)
        self.win.resize(1500,250*(self.button_num//5+1))
        self.button_num+=1

    def get_url(self,headers,page): #获取搜索页缩略图的url,返回url列表
        url=f'https://www.pixiv.net/ajax/search/artworks/{target1}?word={target1}&order=date_d&mode=all&p={page}&s_mode=s_tag&type=all&lang=zh&version=ee57a9ee72abc13ad00d807c0a7a5ecde735f71b'
        headers['referer']=url
        resp=requests.get(url,headers=headers,verify=False,proxies=proxies)
        thumbnail_urls = re.findall(',"url":"(.*?)",',resp.text)
        thumbnail_urls = [thumbnail_urls[i].replace('\\','') for i in range(len(thumbnail_urls))]
        return thumbnail_urls
    
    def img_download(self,img_download_url):
        self.image_download_thread = Image_Download_Thread(img_download_url)
        self.image_download_thread.textsig.connect(self.append_text)
        self.image_download_thread.start()

    def append_text(self, text):
        self.textbrowser1.append(text)
    
    def refresh_progress_bar(self,value):
        self.progress_bar.setValue(value)

if __name__ == "__main__":
    urllib3.disable_warnings()
    target = '原神'
    target1 = urllib.parse.quote(target)
    view = 100
    page = 1
    path_t = 'D:/Pixiv_picture/'+target+'/thumbnail/'
    path_i = 'D:/Pixiv_picture/'+target+'/image/'
    proxies={'https':'127.0.0.1:7890'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
        'cookie':'first_visit_datetime_pc=2023-03-22+23:46:27; p_ab_id=7; p_ab_id_2=7; p_ab_d_id=268037037; yuid_b=JSeGdIU; device_token=fc859ce3cccabbb0c975e25e6645c7b2; privacy_policy_agreement=5; privacy_policy_notification=0; a_type=1; b_type=1; _im_vid=01GW4WJSDKZJ6JJ90AZCF9QWRA; _fbp=fb.1.1679496412837.1254382210; login_ever=yes; _gcl_au=1.1.1444779397.1679496511; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.1701354189.1680181696; __cf_bm=4ApWFpNb5.gCF4sgmpJnzYLH_0SpnGsk8jifXJKzbDQ-1680183694-0-Adyrj7LQcfE4E5Qf5PeoU8bxq6xHOP3mYTtlXsnlx8qD/0JcF/UbVDlZlc7MAQKwBXPeoAaB5bV24JcEGZ6vWWQ5M6me6bfkplhIb5gLBROyNHMeAVkrziew7GQ1Fd1fXR6u7IRe9k/8muxbGtnzY10Rnit7bsV9ZJ4UfMbhA2AdG+xsNaGJfDBF4tSmGKeCaw==; tag_view_ranking=_EOd7bsGyl~0xsDLqCEW6~rRSKPKi9Dv~npWJIbJroU~VRuBtwFc6O~UC88m8Ncjp~t2ErccCFR9~liM64qjhwQ~UniH1CHOF_~j2Cs25NHKk~FXm3-0izvb~ziiAzr_h04~cb-9gnu4GK~b_rY80S-DW~DvbaBUMbjP~dqqWNpq7ul~9JUl9VZvAE~eusCd1AMhu~veODt1WdzX~2GVngxkxTb~59dAqNEUGJ~XhOHJMaDOw~zu--HBEX2K~gf2RRY4mSK~gyXGHTTt7f~tDad2ZQ_GJ~Lt-oEicbBr~TqiZfKmSCg~CkDjyRo6Vc~ZnVEmREUi7~PKZyEOllwO~EjFGSeP9su~KMpT0re7Sq~PFIXHSJMRA~7dpqkQl8TH~7YNsdVv1xN~KacCFmbZiS~azESOjmQSV~5oPIfUbtd6~qLRlQPULHt~fv-doZT2yO~1yo_FtLsad~FE9s9RlCMY~eVxus64GZU~0unkWsk4kG~JrQgdjRZtN~sGOT44B_bo~_zH3D1CHig~r01unnQL0a~5U2rd7nRim~JWOyXSsjO2~faHcYIP1U0~RTJMXD26Ak~rOnsP2Q5UN~TWrozby2UO~KN7uxuR89w~NHNBwIWrH_~lkoWqucyTw~e2syg_rHyV~6293srEnwa~FdBF-J6Pun~VZAPYEMQnQ~m7Ok4YJ8uN~YKP81wwPPT~vUJKYVMOoy~fD8UdX152A~fTz375i7dZ~aPdvNeJ_XM~OgLi_QXWK2~c0RwjBwJgL~MfZWI3Zuez~aWbv1jixtU~eYfNGKUJaM~Ltq1hgLZe3~Te-Gu2wMLd~ByLJlI4pD7~sdPX4119UR~GNcgbuT3T-~NAVlUJuHDQ~4TDL3X7bV9~6RcLf9BQ-w~LtW-gO6CmS~oJAJo4VO5E~ouiK2OKQ-A~HBlflqJjBZ~j0lptk7ELi~KyFwW1QnOO~svvkfO5_78~Ob2dVjBvWQ~7TL10-HUQU~ivS9O2ycg-~1s4b4irzBH~lk1y5y0FPV~Kl6iavssH9~LJo91uBPz4~kOe05XkXBp~3SAZKPd9Ah~_HnoAesBlN~VmlVgqGndA~CiSfl_AE0h; cto_bundle=S4vbhF9nbW50SiUyRlRtd1dBd25oJTJGSUlHJTJCVHFPOTVKVGllejI3NmlKUHN2UHVIeWolMkZ1THFDaFo1akc2NmpDbUZuZzY0RDBYclkyRWVsT1JQTER4eWs0V0hVd2VSWDZsM2hxUURCZlBDZnMzUjNmdEJraHkwWXUlMkZTWjNLZ1NQOXN5bWhPVlE2TjVROWc1dDlPdWdzb0hOSzhsVWlBJTNEJTNE; _ga_MZ1NL4PHH0=GS1.1.1680183742.3.1.1680183777.0.0.0; c_type=25; _gat_UA-1830249-3=1; PHPSESSID=92669508_X03OFCkI3e65wNenaDtXqhYoUyh80ESa; _ga=GA1.2.811011881.1679496389; _ga_75BBYNYN9J=GS1.1.1680181691.7.1.1680183840.0.0.0',
    }
    app = QApplication(sys.argv)
    w=Pixiv()
    w.show()
    app.exec()