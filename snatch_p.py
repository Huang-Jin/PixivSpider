import urllib.request,urllib.error
import re,os
import time
from multiprocessing import Process,Queue

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

def getReferer(url):
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
    reg = r'.+/(\d+)_p0'
    return reference + re.findall(reg,url)[0] + "&page=0"

def saveImage(Urllist,save_path,q,index):
    Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection":"keep-alive",
               "Referer":""}
    i = 0
    fails = 0
    repeat_times = 2
    for x in Urllist:
        x=x.replace('c/240x480/img-master','img-original')
        x=x.replace('_master1200','')
        Headers['Referer'] = getReferer(x)
        begin_time1 = time.time()
        fail = 0
        try:
            try:
                req = urllib.request.Request(x, None, Headers)
                res = urllib.request.urlopen(req, timeout=1)
                res.close()
            except urllib.error.HTTPError:
                x = x.replace('.jpg', '.png')
                req = urllib.request.Request(x, None, Headers)
                res = urllib.request.urlopen(req, timeout=1)
                res.close()
        except:
            continue
        i += 1
        image_path = save_path + '/%s%s' % (index + i, os.path.splitext(x)[1])

        for j in range(1,repeat_times+1):
            try:
                res = urllib.request.urlopen(req, timeout=1)
                rstream = res.read()
                res.close()
                break
            except:
                res.close()
                fail += 1
                print('repeat index %d -- %d.' % (index+i,fail))

        if(fail==repeat_times):
            print('%d\t%s\tdownload image failed.' %
                (index + i, x))
            fails += 1
            continue
        with open(image_path, 'wb') as f:
            f.write(rstream)
        end_time1 = time.time()
        print('%d\t%s\tdownload image costs %.2f seconds' %
              (index + i, x, end_time1 - begin_time1))
    print('Index %d to %d have been saved into files\t%d failed.\tProcess Over!...' % (index+1,index+i,fails))
    q.put(fails)

def getPixivImages(date):
    start = time.time()
    pagecount = 10
    page = 1
    index = 0
    save_path = './original_images/%s%02d%02d' % (date.year, date.month, date.day)
    # ex_path = save_path.replace('pixiv_images/','pixiv_images/excellent/')
    if not (os.path.exists(save_path)):
        print(save_path+" now starts.")
        os.mkdir(save_path)
    else:
        print(save_path[-8::] + ' has been already retrieved.')
        return None
        # pass
    q=Queue()
    ps=[]
    reg = re.compile(r'class="new".+?data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
    while page<=pagecount and index < 100:
        html = getHtml("http://www.pixiv.net/ranking.php?mode=daily&"
                       "content=illust&p=%d&date=%s%02d%02d" % (page,date.year, date.month, date.day))
        imgurl = re.findall(reg, html)
        print(len(imgurl))
        p=Process(target=saveImage,args=(imgurl,save_path,q,index))
        p.start()
        ps.append(p)
        index += len(imgurl)
        page+=1
    for p in ps:
        p.join()
    end = time.time()

    fails = 0
    while not q.empty():
        item = q.get()
        fails += item

    if index!=0:
        print('Process getPixiv costs %.2f second with %d images\n'
          'Every picture costs %.2f second\n'
              '%d images failed.' % ((end-start),index,(end-start)/(index),fails))
    else:
        print('%s%02d%02d has no new images...' % (date.year, date.month, date.day))
        os.rmdir(save_path)

if __name__ == '__main__':
    # socket.setdefaulttimeout(1)
    pass
    # test
    # urllib.request.urlopen('http://i3.pixiv.net/img-original/img/2017/01/20/10/05/15/61020086_p0.jpg')

    # os.system('pause')

