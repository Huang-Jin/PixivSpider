import snatch_p
import datetime,os

if __name__ == '__main__':
    try:
        date = datetime.datetime.now()
        snatch_p.getPixivImages(date - datetime.timedelta(days=2))
    except:
        print('some error was traced.')
    os.system('pause')