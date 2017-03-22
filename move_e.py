import os,shutil
import configparser

if __name__ == '__main__':
    config_path = './config_files/move.cfg'
    save_path = './original_images/excellent'
    image_path = './ep_images'
    i_num = 0
    for dirpath, dirnames, filenames in os.walk(image_path):
        for filename in filenames:
            fpath = os.path.join(dirpath,filename)
            i_num += 1
            current_path = save_path + '/%s%s' % (i_num,os.path.splitext(fpath)[1])
            shutil.move(fpath,current_path)
            print(fpath + '\t-->\t' + current_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set('image','num','0')
    with open(config_path,'w') as cf:
        config.write(cf)
    os.system('pause')