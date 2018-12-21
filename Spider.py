import re
import os
import time
from multiprocessing import Process, Queue
import threading
from urllib import request, error
from tqdm import tqdm


class Spider:
    def __init__(self):
        pass

    @staticmethod
    def get_html(url):
        page = request.urlopen(url)
        html = page.read().decode('utf-8')
        return html


# class MultiProcessPixivSpider(Spider):
#
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
#                              '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
#                "Connection": "keep-alive",
#                "Referer": ""}
#
#     @staticmethod
#     def get_referer(url):
#         reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
#         reg = r'.+/(\d+)_p0'
#         return reference + re.findall(reg, url)[0] + "&page=0"
#
#     def save_image(self, urls, save_path, q, index):
#         i = 0
#         fails = 0
#         repeat_times = 2
#         pbar = tqdm(total=100)
#         for url in urls:
#             url = url.replace('c/240x480/img-master', 'img-original')
#             url = url.replace('_master1200', '')
#             self.headers['Referer'] = self.get_referer(url)
#             begin_time1 = time.time()
#             fail = 0
#             try:
#                 try:
#                     req = request.Request(url, None, self.headers)
#                     res = request.urlopen(req, timeout=1)
#                     res.close()
#                 except error.HTTPError:
#                     url = url.replace('.jpg', '.png')
#                     req = request.Request(url, None, self.headers)
#                     res = request.urlopen(req, timeout=1)
#                     res.close()
#             except:
#                 continue
#             i += 1
#             image_path = save_path + '/%s%s' % (index + i, os.path.splitext(url)[1])
#
#             for j in range(0, repeat_times):
#                 try:
#                     res = request.urlopen(req, timeout=1)
#                     rstream = res.read()
#                     res.close()
#                     break
#                 except:
#                     res.close()
#                     fail += 1
#                     # print('repeat index %d -- %d.' % (index + i, fail))
#
#             if fail == repeat_times:
#                 # print('%d\t%s\tdownload image failed.'
#                 #       % (index + i, url))
#                 fails += 1
#             else:
#                 with open(image_path, 'wb') as f:
#                     f.write(rstream)
#                 end_time1 = time.time()
#                 # print('%d\t%s\tdownload image costs %.2f seconds'
#                 #       % (index + i, url, end_time1 - begin_time1))
#             pbar.update(1)
#         pbar.close()
#
#         # print('Index %d to %d have been saved into files\t%d failed.\tProcess Over!...'
#         #       % (index + 1, index + i, fails))
#         q.put(fails)
#
#     def get_pixiv_images(self, date):
#         try:
#             start = time.time()
#             pagecount = 10
#             page = 1
#             index = 0
#             save_path = './original_images/%s%02d%02d' % (date.year, date.month, date.day)
#             # ex_path = save_path.replace('pixiv_images/','pixiv_images/excellent/')
#             if not (os.path.exists(save_path)):
#                 print(save_path + " now starts.")
#                 os.makedirs(save_path)
#             else:
#                 print(save_path[-8::] + ' has been already retrieved.')
#                 return None
#                 # pass
#             q = Queue()
#             ps = []
#             reg = re.compile(
#                 r'class="new".+?data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
#             while page <= pagecount and index < 100:
#                 html = self.get_html("http://www.pixiv.net/ranking.php?mode=daily&"
#                                      "content=illust&p=%d&date=%s%02d%02d" % (page, date.year, date.month, date.day))
#                 imgurl = re.findall(reg, html)
#                 # print(len(imgurl))
#                 p = Process(target=self.save_image, args=(imgurl, save_path, q, index))
#                 p.start()
#                 ps.append(p)
#                 index += len(imgurl)
#                 page += 1
#
#             for p in ps:
#                 p.join()
#             end = time.time()
#
#             fails = 0
#             while not q.empty():
#                 item = q.get()
#                 fails += item
#
#             if index != 0:
#                 print('Processing costs %.2f second with %d images, %.2f second in average\n'
#                       '%d images failed.' % ((end - start), index, (end - start) / index, fails))
#             else:
#                 print('%s%02d%02d has no new images...' % (date.year, date.month, date.day))
#                 os.rmdir(save_path)
#         except:
#             raise Exception("Exception occured when scatching images.")

class MultiThreadPixivSpider(Spider):
    lock = threading.Lock()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
               "Referer": ""}

    @staticmethod
    def get_pixiv_id(url):
        reg = r'.+/(\d+)_p0'
        return re.findall(reg, url)[0]

    def get_referer(self, url):
        reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
        return reference + self.get_pixiv_id(url) + "&page=0"

    def save_image(self, urls, save_path, q, pbar):
        # self.lock.acquire()  # Make sure the lock will be released.
        # try:
            i = 0
            fails = 0
            repeat_times = 2

            for url in urls:
                url = url.replace('c/240x480/img-master', 'img-original')
                url = url.replace('_master1200', '')
                self.headers['Referer'] = self.get_referer(url)
                # begin_time1 = time.time()
                fail = 0
                try:
                    try:
                        req = request.Request(url, None, self.headers)
                        res = request.urlopen(req, timeout=1)
                        res.close()
                    except error.HTTPError:
                        url = url.replace('.jpg', '.png')
                        req = request.Request(url, None, self.headers)
                        res = request.urlopen(req, timeout=1)
                        res.close()
                except:
                    pbar.update(1)
                    i += 1
                    fails += 1
                    continue
                i += 1
                image_path = save_path + '/%s%s' % (self.get_pixiv_id(url), os.path.splitext(url)[1])

                for _ in range(0, repeat_times):
                    try:
                        res = request.urlopen(req, timeout=1)
                        rstream = res.read()
                        res.close()
                        break
                    except:
                        res.close()
                        fail += 1
                        # print('repeat index %d -- %d.' % (index + i, fail))

                if fail == repeat_times:
                    # print('%d\t%s\tdownload image failed.'
                    #       % (index + i, url))
                    fails += 1
                else:
                    with open(image_path, 'wb') as f:
                        f.write(rstream)
                        # end_time1 = time.time()
                        # print('%d\t%s\tdownload image costs %.2f seconds'
                        #       % (index + i, url, end_time1 - begin_time1))
                pbar.update(1)

            # print('Index %d to %d have been saved into files\t%d failed.\tProcess Over!...'
            #       % (index + 1, index + i, fails))
            q.put(fails)
        # finally:
        #     self.lock.release()

    def get_pixiv_images(self, date):
        try:

            start = time.time()
            pagecount = 10
            page = 1
            index = 0

            save_path = './original_images/%s%02d%02d' % (date.year, date.month, date.day)
            if not (os.path.exists(save_path)):
                print(save_path + " now starts.")
                os.makedirs(save_path)
            else:
                print(save_path[-8::] + ' has been already retrieved.')
                return None

            q = Queue()  # The communication between threadings, mainly the number of failings when catching image
            ps = []  # As we didn't know how much threads needed, a dynamic list is necessary.
            indexes = []  # Beginning indexes for each threading.
            imgurls = []

            reg = re.compile(
                r'class="new".+?data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')

            while page <= pagecount and index < 100:
                html = self.get_html("http://www.pixiv.net/ranking.php?mode=daily&"
                                     "content=illust&p=%d&date=%s%02d%02d" % (page, date.year, date.month, date.day))
                imgurl = re.findall(reg, html)
                # print(len(imgurl))
                imgurls.append(imgurl)
                indexes.append(index)
                index += len(imgurl)
                page += 1

            pbar = tqdm(total=index, ascii=True)
            for i in range(len(indexes)):
                p = threading.Thread(target=self.save_image, args=(imgurls[i], save_path, q, pbar))
                p.start()
                ps.append(p)
            for p in ps:
                p.join()
            end = time.time()
            pbar.close()

            fails = 0
            while not q.empty():
                item = q.get()
                fails += item

            if index != 0:
                print('Processing costs %.2f second with %d images, %.2f second in average\n'
                      '%d images failed.' % ((end - start), index, (end - start) / index, fails))
            else:
                print('%s%02d%02d has no new images...' % (date.year, date.month, date.day))
                os.rmdir(save_path)
        except:
            raise Exception("Exception occured when scatching images.")


if __name__ == '__main__':
    pass
