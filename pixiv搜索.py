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
    id_sign = pyqtSignal(str)
    textsig = pyqtSignal(str)
    def __init__(self,thumbnail_urls):
        super().__init__()
        self.thumbnail_urls = thumbnail_urls

    def thumbnail_download(self,thumbnail_url):
        id=thumbnail_url.split('/')[-1].split('_')[0] #获取图片id
        file=path_t+id+'.jpg' #获取文件路径
        img_url = 'https://www.pixiv.net/artworks/'+id
        resp = requests.get(img_url,headers=headers)
        viewcount = re.search('"viewCount":(.*?),',resp.text).group(1)
        if int(viewcount)>view:
            img_download_url = re.search('"original":"(.+?)"',resp.text).group(1)
            thumbnail_=requests.get(thumbnail_url,headers=headers,proxies=proxies)
            if os.path.isfile(file)==True:
                self.textsig.emit(f'{id}已存在,{viewcount}')
            else:
                with open(file,'wb') as f:
                    f.write(thumbnail_.content)
                self.textsig.emit(f'{id}已下载,{viewcount}')
            self.id_sign.emit(str(img_download_url))

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
        self.thumbnail_urls = self.get_url(headers,page)
        self.thumbnail_list = os.listdir(path_t)
        self.button_num = 0
        self.initUI()
    
    def initUI(self):
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.setWindowTitle("Pixiv_搜索")
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

        self.win.setLayout(self.grid)
        self.scrollarea.setWidget(self.win)
        self.thumbnail_download_thread = Thumbnail_Download_Thread(self.thumbnail_urls)
        self.thumbnail_download_thread.id_sign.connect(self.addimgbutton)
        self.thumbnail_download_thread.textsig.connect(self.append_text)
        self.thumbnail_download_thread.start()

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

if __name__ == "__main__":
    urllib3.disable_warnings()
    target = '温迪'
    page = 1
    view = 100
    path_t = 'D:/'+target+'/thumbnail/'
    path_i = 'D:/'+target+'/image/'
    target1 = urllib.parse.quote(target)
    if os.path.isdir(path_t)==False:
        os.makedirs(path_t)
    if os.path.isdir(path_i)==False:
        os.mkdir(path_i)
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