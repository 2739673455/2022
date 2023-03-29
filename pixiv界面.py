# Pixiv图片界面
import os
import re
import sys
import urllib3
import requests
import concurrent.futures
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Thumbnail_Download_Thread(QThread): #下载预览图线程
    id_sign = pyqtSignal(str)
    textsig = pyqtSignal(str)
    def __init__(self,thumbnail_urls):
        super().__init__()
        self.thumbnail_urls = thumbnail_urls

    def thumbnail_download(self,thumbnail_url):
        id=thumbnail_url.split('/')[-1].split('_')[0] #获取图片id
        file=path+id+'.jpg' #获取文件路径
        if os.path.isfile(file)==True:
            self.textsig.emit(f'{id}已存在')
        else:
            thumbnail_1=requests.get(thumbnail_url,headers=headers,proxies=proxies)
            with open(file,'wb') as f:
                f.write(thumbnail_1.content)
            self.textsig.emit(f'{id}已下载')
            self.id_sign.emit(str(id))

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.thumbnail_download, url) for url in self.thumbnail_urls]

class Image_Download_Thread(QThread): #下载高清图线程
    textsig = pyqtSignal(str)
    def __init__(self,id):
        super().__init__()
        self.id = id

    def run(self):
        url= f'https://www.pixiv.net/artworks/{self.id}'
        path2='D:/Pixiv_top50/img/'
        if os.path.isdir(path2)==False:
            os.mkdir(path2)
        file2 = path2+self.id+'.jpg'
        if os.path.isfile(file2)==True:
            self.textsig.emit(f'{self.id}已存在{path2}')
        else:
            headers['referer']=url
            resp1=requests.get(url,headers=headers,verify=False,proxies=proxies)
            resp2=re.search('"original":"(.+?)"',resp1.text)
            resp2=resp2.group(1)
            s = requests.get(resp2,headers=headers,verify=False,proxies=proxies)
            with open(file2,'wb') as f:
                f.write(s.content)
            self.textsig.emit(f'{self.id}下载至{path2}')
            s.close()

class Pixiv(QDialog):
    def __init__(self):
        super().__init__()
        self.id_dict = dict()
        self.thumbnail_urls = self.get_url(headers)
        self.thumbnail_list = os.listdir(path)
        self.i = 0
        self.initUI()
    
    def initUI(self):
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.setWindowTitle("Pixiv_top50")
        self.resize(1600,1200)
        self.layout1 = QVBoxLayout()

        self.scrollarea = QScrollArea(self)
        self.win = QWidget()
        self.grid = QGridLayout()

        self.textbrowser1 = QTextBrowser()
        self.textbrowser1.setFixedSize(1500,200)

        self.layout1.addWidget(self.scrollarea)
        self.layout1.addWidget(self.textbrowser1)
        self.setLayout(self.layout1)

        for j in range(len(self.thumbnail_list)):
            self.addimgbutton(self.thumbnail_list[j].split('.')[0])

        self.win.setLayout(self.grid)
        self.scrollarea.setWidget(self.win)
        self.thumbnail_download_thread = Thumbnail_Download_Thread(self.thumbnail_urls)
        self.thumbnail_download_thread.id_sign.connect(self.addimgbutton)
        self.thumbnail_download_thread.textsig.connect(self.append_text)
        self.thumbnail_download_thread.start()

    def addimgbutton(self,id): #添加按钮
        thumbnail = path+id
        self.button1 = QPushButton()
        self.button1.setIcon(QIcon(thumbnail))
        self.button1.setIconSize(QSize(250,400))
        self.id_dict[thumbnail] = id
        self.button1.clicked.connect(lambda x=thumbnail:self.img_download(self.id_dict[thumbnail]))
        self.grid.addWidget(self.button1,self.i//5,self.i%5)
        self.win.resize(1500,400*(self.i//5+1))
        self.i+=1

    def get_url(self,headers): #获取排行榜前五十的作品缩略图的url,返回url列表
        url='https://www.pixiv.net/ranking.php?mode=daily_r18'
        headers['referer']=url
        resp=requests.get(url,headers=headers,verify=False,proxies=proxies)
        thumbnail_urls=re.findall('"data-filter="thumbnail-filter lazy-image"data-src="(.*?)"data-type="illust"data-id="',resp.text,re.S)
        return thumbnail_urls
    
    def img_download(self,id):
        self.image_download_thread = Image_Download_Thread(id)
        self.image_download_thread.textsig.connect(self.append_text)
        self.image_download_thread.start()

    def append_text(self, text):
        self.textbrowser1.append(text)

if __name__ == "__main__":
    urllib3.disable_warnings()
    path = "D:/Pixiv_top50/thumbnail/"
    if os.path.isdir(path)==False:
        os.makedirs(path)
    proxies={'https':'127.0.0.1:7890'}
    headers={
    'Connection':'close',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'cookie': 'first_visit_datetime_pc=2022-12-15+20:36:48; p_ab_id=3; p_ab_id_2=7; p_ab_d_id=815045519; yuid_b=QHdmlZM; __utmz=235335808.1671104212.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=25093650_mhfz1BbsvI13yOlSjF4tylzwfPtP6gmS; device_token=3fad70a5ea88a5cd26b7010a4b0b2c7b; privacy_policy_agreement=5; _ga_MZ1NL4PHH0=GS1.1.1671104213.1.0.1671104216.0.0.0; c_type=32; privacy_policy_notification=0; a_type=1; b_type=1; __utmv=235335808.|2=login ever=no=1^3=plan=normal=1^5=gender=male=1^6=user_id=25093650=1^9=p_ab_id=3=1^10=p_ab_id_2=7=1^11=lang=zh=1; _fbp=fb.1.1671104216530.1386501833; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _im_vid=01GMAS5JTHACVBKHHJVG4AJDJW; _im_uid.3929=h.e6658c04c1308c0c; adr_id=uTbg186QFFz1PjBL5xPZ11nRgV2rEY9Ck4baiyMbporOqzZU; tag_view_ranking=0xsDLqCEW6~_EOd7bsGyl~5oPIfUbtd6~txZ9z5ByU7~cb-9gnu4GK~RTJMXD26Ak~c7QmKEJ54V~faHcYIP1U0~WVrsHleeCL~BSlt10mdnm~CiSfl_AE0h~6293srEnwa~jy1Ljjlbd1~kVBgVYqL2q~RxQtPoROWu~tN9MyonktM~ijb1Y04gkD~rT9WTjeTAD~PTyxATIsK0~dXoVfWNqZx~0Sds1vVNKR~d9UpgqVAEz~-sp-9oh8uv~Ltq1hgLZe3~Bd2L9ZBE8q~UcTTPypj4n~E1yS6jImG-~dDxAe02g2b~x5Jrzac4QC~U02eb9uf9U~pzZvureUki~Cac_6jhDcg~DADQycFGB0~QaiOjmwQnI~zvgW9BzK6h; cto_bundle=l5O99F9uakRXbVphSWR0JTJCWVAxRTUwSHNDYllJNkR2R0dwaUJCMTQ1cFhLc01ncmNYMnBaJTJCc1Q0Q1BCQnVCaWxKbEVXT1JrNFZnJTJCRGJvbWptUVhZTHhEeDQ4JTJCQU8lMkJSbUhtT3lIeXFvbGpBd1ZCJTJGR09EQ2pCVEFIMUdNOGVVcWRzdEdESmlMSzY5RTJLbzJCM05uempydSUyQm1JQSUzRCUzRA; _ga=GA1.1.696882263.1671104211; __utma=235335808.696882263.1671104211.1671104212.1671199686.2; __utmc=235335808; __utmt=1; __utmb=235335808.2.10.1671199686; __cf_bm=0eKBagUPrTdLqVHt1hNX43ToZMarQARnjlJguflh.9I-1671200031-0-AThTWk0iHwrmyySKi6Zl/RMeAPMo4UQR5Rrz+lhkwOkCSLI8MJlTwpD/fFaaPjQEIiHBiEAnNuqu0AUgWp7goMFWcShZRzUogswAi1dNRCsOnasKMNtik+UBNZ+wfv/3NDJtJxcpBefAoapSXeDZ1tl8Vq45DVn2D06WhO6u22Rn2pR3ZTjFxgxGOA96yKz0Vd1k54RxonJAAVrLftCj8Ew=; _ga_75BBYNYN9J=GS1.1.1671198837.2.1.1671200053.0.0.0',
    # 'referer': f'{url}'
    }
    app = QApplication(sys.argv)
    w=Pixiv()
    w.show()
    app.exec()