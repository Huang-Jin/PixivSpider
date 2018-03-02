from Spider import MultiThreadPixivSpider
import datetime
import configparser
import os

# get next date's images
# begin from 'begindate'

if __name__ == '__main__':

    config_path = './config_files/next.cfg'
    config = configparser.ConfigParser()
    config.read(config_path)

    begindate = datetime.datetime(
        config.getint('date', 'year'),
        config.getint('date', 'month'),
        config.getint('date', 'day')
    )

    i = 1
    now_date = begindate + datetime.timedelta(days=i)

    spider = MultiThreadPixivSpider()
    while True:
        config.set('date', 'year', str(now_date.year))
        config.set('date', 'month', str(now_date.month))
        config.set('date', 'day', str(now_date.day))
        try:
            spider.get_pixiv_images(now_date)
        except:
            print("The date --" + now_date.strftime("%Y/%m/%d") + "-- has no data.")
            break
        with open(config_path, 'w') as cf:
            config.write(cf)
        i += 1
        now_date = begindate + datetime.timedelta(days=i)

    os.system("pause")
