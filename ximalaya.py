from bs4 import BeautifulSoup
import requests
import os
import threading
import multiprocessing
import time
# 爬取的连接
baseurl = 'https://www.ximalaya.com/xiqu/49205494/'
# 开始页码
start_page = 1
# 结束页码（包含结束页码）
end_page = 1
# 最大开启线程数，推荐为cpu核数
max_downloads_number = 8
# 下载地址
download_dict = "F://代码//python代码//music//豫剧//"
########################以下是逻辑代码#################################
total_num = 0 # 总任务数
finished_num = multiprocessing.Value("d", 0) # 下载完成数目
start = time.perf_counter() # 开始计时
# 定义进度条
def progress_bar(finish_tasks_number, tasks_number):
    scale = 100/tasks_number
    percentage = round(finish_tasks_number / tasks_number * 100)
    finished_label = "▓" * round(finish_tasks_number*scale)
    unfinished_label = "-" * int(100 - round(finish_tasks_number*scale))
    duration = time.perf_counter() - start
    print("\r{}% [{}{}] {:.2f}s".format(percentage, finished_label, unfinished_label,duration), end="")
#网页解析
def getHTML(url):
    try:
        headers = {'User-Agent':'Unnecessary semicolonMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
        r=requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except:
        return "产生异常"
# 下载
def getMp3(name2,url):
    root = download_dict
    path = root + name2+'.m4a'
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            headers = {'User-Agent':'Unnecessary semicolonMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
            r=requests.get(url, headers = headers)
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
    except:
        print("爬取失败")
    finished_num.value +=1
    progress_bar(finished_num.value, total_num)
# 获取连接
list1 = []
def get_M4a_Url(s):
    soup = BeautifulSoup(s, "html.parser")
    for link in soup.find_all(attrs={'class':'text Mi_'}):
        name1=link.a.get('title')
        id1=link.a.get('href').split('/')[-1]
        src='https://www.ximalaya.com/revision/play/v1/audio?id='+str(id1)+'&ptype=1'
        audiodic=getHTML(src)
        src1 = audiodic.json()['data']['src']
        my_dict={"name":name1,'id':id1,'src':src1}
        list1.append(my_dict)
    return list1
# 开启多线程
threads=[]
for i in range(start_page,end_page+1):
  print('\033[1;34m正在解析第'+str(i)+'页\033[0m')
  if i==1:
    src = baseurl
  else:
    src=baseurl+'p'+str(i)
  s=getHTML(src).text
  get_M4a_Url(s)
  print('\033[1;35m第'+str(i)+'页解析完毕\033[0m')
total_num = len(list1)
print('\033[1;35m共'+str(total_num)+'条数据\033[0m')
for dict2 in list1:
    t = threading.Thread(target=getMp3, args=(dict2['name'],dict2['src'],))
    threads.append(t)
for t in threads:
    t.start()
    while True:
      if(len(threading.enumerate()) <= max_downloads_number):
        break

