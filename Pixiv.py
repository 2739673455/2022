from tkinter import *
from PIL import Image,ImageTk
import os
import requests
import re
import urllib3
from threading import Thread
urllib3.disable_warnings()
path='D:/ztop50'
# 判断路径是否存在
if os.path.isdir(path)==False:
    os.mkdir(path)

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
    'cookie': 'first_visit_datetime_pc=2022-10-02+22%3A50%3A16; p_ab_id=7; p_ab_id_2=9; p_ab_d_id=1498094093; yuid_b=GJgwc2A; _gcl_au=1.1.1821310679.1664718627; _fbp=fb.1.1664718627620.323179474; privacy_policy_agreement=5; PHPSESSID=25093650_8xevCOUeRNLragJskYUxbhuLBXgpns6Y; c_type=31; privacy_policy_notification=0; a_type=1; b_type=1; _im_vid=01GECFDA6S9WN9PH9P9ZCQXJ65; adr_id=N1s4562PSPkGluUsOa715wILBMwMy4wrWJcCU7Fk2Z2bQTi1; login_ever=yes; pt_60er4xix=uid=ZtdQ4fYG6kpamHw4C/EEug&nid=1&vid=/fmgZvIDvEA9uwm7ixSAkQ&vn=1&pvn=1&sact=1667309581788&to_flag=0&pl=IZoRf4OCSv6aouL5bhDEAg*pt*1667309581788; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.1107917886.1667657581; cto_bundle=oO1GX195UmtwRnclMkZWN0xZdmN6NXhzZVdQOUtLVldwOWJSa01jcmM5UVJpWVNkeDVsYmU5aUxkZHU3Tkxrdm4yekVHZVp0WGo1ZHE1b2o0RkRsc3V0UyUyRlc4ZWRScE1wRDBsRE15ZlBBWHJnZVdhU0RZZ24xUUcyRndwdlcyV0pHOXpJUHBGSlpyMUl4RyUyQldhT0YlMkJSaTRSdEVGQSUzRCUzRA; cto_bundle=oO1GX195UmtwRnclMkZWN0xZdmN6NXhzZVdQOUtLVldwOWJSa01jcmM5UVJpWVNkeDVsYmU5aUxkZHU3Tkxrdm4yekVHZVp0WGo1ZHE1b2o0RkRsc3V0UyUyRlc4ZWRScE1wRDBsRE15ZlBBWHJnZVdhU0RZZ24xUUcyRndwdlcyV0pHOXpJUHBGSlpyMUl4RyUyQldhT0YlMkJSaTRSdEVGQSUzRCUzRA; tag_view_ranking=_EOd7bsGyl~cb-9gnu4GK~0xsDLqCEW6~ziiAzr_h04~UC88m8Ncjp~e2syg_rHyV~ZnVEmREUi7~6293srEnwa~gCB7z_XWkp~D0nMcn6oGk~Xtj8k6R-Wf~59dAqNEUGJ~RgayaGNSdm~TqiZfKmSCg~DVBgrmJ4IG~Lt-oEicbBr~1HSjrqSB3U~j2Cs25NHKk~9Gbahmahac~IZL19yApOk~_zH3D1CHig~o7hvUrSGDN~HY55MqmzzQ~QaiOjmwQnI~jmp1v87V2T~eYfNGKUJaM~jk9IzfjZ6n~zdx7NJPPfr~NYmhNFy47T~4i9bTBXFoE~MnGbHeuS94~2kSJBy_FeR~CMvJQbTsDH~W8j4ADUfUR~5oPIfUbtd6~4TDL3X7bV9~rIC2oNFqzh~G_tI3i2Q6c~fS_H2TuIRD~RTJMXD26Ak~BnnLTcipFS~sGOT44B_bo~PwDMGzD6xn~6GYRfMzuPl~48UjH62K37~rOnsP2Q5UN~WmLE2Ds3a1~DlTwYHcEzf~aqS7-jy_iF~I5WYPjM2n2~gnmsbf1SSR~qWFESUmfEs~azESOjmQSV~YUuqn7At7n~Ie2c51_4Sp~BSlt10mdnm~XGIFyGsM9U~eVxus64GZU~6HUSQEiWHT~UniH1CHOF_~t2ErccCFR9~lkoWqucyTw~vUJKYVMOoy~bfM8xJ-4gy~tN9MyonktM~RxQtPoROWu~pzZvureUki~pGv7p05oAU~JrQgdjRZtN~oCqKGRNl20~Z64uUp2DUX~zd0kMkvoqd~zb1N_JZSZu~rM47Mg3Mj4~QFQIGuIyUn~txZ9z5ByU7~fPLHON4XyJ~yas9urq5RE~STvOPg9Ijz~zyKU3Q5L4C~jy1Ljjlbd1~vQ8AwyNxCM~LX3_ayvQX4~dg_40nEhSE~a3zvshTj4U~r5GFgFyoSE~xha5FQn_XC~HZk-7ZdqP6~7PLip1x0SZ~_hSAdpN9rx~Fuu81ZA3JD~ZOwCtwovNC~q3eUobDMJW~RDY8AkVSDu~yREQ8PVGHN~npWJIbJroU~Ltq1hgLZe3~OFI5amF0sJ~XDEWeW9f9i~-StjcwdYwv; __cf_bm=D7CkKKFh8OtNmXSdn4loGRds3R2njEV1I.uJOXzyJis-1667660974-0-AUIlC+I9pDMq5of72kgKii+b0a0FUJhS3FdpIXXxronvnt6AgiNDQvNmJrD0wXyinAip9wQyOT+U6ZnjALfoyhS2EyxAAgsCW4AqiS2dh9yqEnlgmAbjciJ/p2RJ58s8re5Of/DHzXIKMdALq+Cs1LT6ZDnZdPYm0wK37teR4TJnswVhun6qU51Hb8uXOIpaUg==; _ga=GA1.2.1568050040.1664718627; _ga_75BBYNYN9J=GS1.1.1667660893.33.1.1667661051.0.0.0',
    # 'referer': f'{url}'
}

# 下载图片至D:/top50
def download_picture(url,headers=headers):
    url= f'https://www.pixiv.net/artworks/{url}'
    name=url.rsplit('/',1)[-1]
    path='D:/top50'
    # 判断路径是否存在
    if os.path.isdir(path)==False:
        os.mkdir(path)
    # 判断文件是否存在
    if os.path.isfile(f'D:/top50/{name}.jpg')==True:
        print(f'{name}已存在')
    else:
        headers['referer']=url
        resp1=requests.get(url,headers=headers,verify=False)
        resp2=re.search('"original":"(.+?)"',resp1.text)
        resp2=resp2.group(1)
        s = requests.get(resp2,headers=headers,verify=False)
        with open(f'D:/top50/{name}.jpg','wb') as f:
            f.write(s.content)
        print(f'{name}下载完成')
        s.close()

# 获取排行榜前五十的作品缩略图和id,返回列表
def get_url(headers):
    url='https://www.pixiv.net/ranking.php?mode=daily_r18'
    headers['referer']=url
    resp=requests.get(url,headers=headers)
    thumbnail=re.findall('"data-filter="thumbnail-filter lazy-image"data-src="(.*?)"data-type="illust"data-id="',resp.text,re.S)
    return thumbnail

# 下载缩略图并显示
files=[]
dict_file={}
def thumbnail_download(n1,n2):
    global files
    global dict_file
    for i in range(n1,n2):
        thumbnail_name=thumbnail[i].split('/')[-1] #获取文件名
        file=path+'/'+thumbnail_name #获取文件路径
        files.append(file)
        dict_file[file]=file.rsplit('/',1)[-1].split('_',1)[0]
        if os.path.isfile(file)==True:
            print(f'{thumbnail_name}已存在')
        else:
            thumbnail_1=requests.get(thumbnail[i],headers=headers)
            with open(file,'wb') as f:
                f.write(thumbnail_1.content)
            print(f'{thumbnail_name}下载完成')

def show_thumbnail():
    for i,file in enumerate(files):
        img_open=Image.open(file)
        img_list[i]=ImageTk.PhotoImage(img_open)
        image=Button(text,image=img_list[i],command = lambda x=file: download_picture(dict_file[x]))
        text.window_create(END,window=image)

win=Tk()
win.title('Pixiv')

scroll=Scrollbar(win)
scroll.pack(side=RIGHT,fill=Y)
text=Text(win,yscrollcommand = scroll.set,width=100,height=50)

thumbnail=get_url(headers)
img_list=[0]*len(thumbnail)

download_threads=[]
for i in range(0,len(thumbnail),len(thumbnail)//10):
    download_thread=Thread(target=thumbnail_download,args=(i,i+5))
    download_threads.append(download_thread)
    download_thread.start()

for download_thread in download_threads:
    download_thread.join()

show_thumbnail()
text.pack(side=LEFT,fill=BOTH,expand=YES)
scroll.config(command =text.yview)

win.mainloop()
