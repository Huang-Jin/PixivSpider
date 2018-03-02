from Spider import MultiThreadPixivSpider
import datetime
import configparser
import os

# get previous date's images
# begin from 'begindate'

if __name__ == '__main__':
    config_path = './config_files/pre.cfg'
    config = configparser.ConfigParser()
    config.read(config_path)
    begindate = datetime.datetime(
        config.getint('date', 'year'),
        config.getint('date', 'month'),
        config.getint('date', 'day')
    )
    i = 1
    spider = MultiThreadPixivSpider()
    now_date = begindate - datetime.timedelta(days=i)
    try:
        while True:
            config.set('date', 'year', str(now_date.year))
            config.set('date', 'month', str(now_date.month))
            config.set('date', 'day', str(now_date.day))
            with open(config_path, 'w') as cf:
                config.write(cf)
                spider.get_pixiv_images(now_date)
            i += 1
            now_date = begindate - datetime.timedelta(days=i)
    except:
        print("Scatching" + now_date.strftime("%Y-%m-%d") + ", unkown Error Occured.")
    os.system("pause")
