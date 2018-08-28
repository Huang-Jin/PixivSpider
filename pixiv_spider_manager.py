import os
import time
import datetime
from Spider import MultiThreadPixivSpider

if __name__ == '__main__':
    print("-")
    print("--")
    print("---Welcome to use the Pixiv Manager!")
    print("---It was written by Jin Huang.")
    print("---You can catch images from pixiv.net by inputting the date you need.")
    print("---The format should like this: 2018/02/26 or just type \"Enter\" for today.")
    print("--")
    print("-\n")

    spider = MultiThreadPixivSpider()
    while True:
        user_input = input("Which date do you want to catch?\n")
        date = datetime.datetime.now()

        if user_input == 'q':
            print("Thank you for using.")
            break

        if user_input != '':
            try:
                date = time.strptime(user_input, "%Y/%m/%d")
            except:
                print("Input is illegal, please try again!")
                continue

            date = datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
        try:
            spider.get_pixiv_images(date)
        except:
            print("An error occured, maybe there are no images in selected day yet.")

    os.system("pause")
