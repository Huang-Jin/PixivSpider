import snatch_p
import datetime
import configparser

# get previous date's images
# begin from 'begindate'

if __name__ == '__main__':
    config_path = './config_files/pre.cfg'
    config = configparser.ConfigParser()
    config.read(config_path)
    begindate = datetime.datetime(
        config.getint('date','year'),
        config.getint('date', 'month'),
        config.getint('date', 'day')
    )
    i=1
    while True:
        now_date = begindate-datetime.timedelta(days=i)
        config.set('date','year',str(now_date.year))
        config.set('date','month',str(now_date.month))
        config.set('date','day',str(now_date.day))
        with open(config_path,'w') as cf:
            config.write(cf)
        snatch_p.getPixivImages(now_date)
        i += 1
