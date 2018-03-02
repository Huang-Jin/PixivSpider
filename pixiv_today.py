from Spider import MultiThreadPixivSpider
import datetime
import os

if __name__ == '__main__':
    try:
        date = datetime.datetime.now()
        spider = MultiThreadPixivSpider()
        spider.get_pixiv_images(date - datetime.timedelta(days=2))
    except:
        print('some error was traced.')
    os.system('pause')
