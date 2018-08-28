import os,shutil
import configparser

def move_from_excellent_to_ep():
    config_path = './config_files/move.cfg'
    image_path = './original_images/excellent'
    save_path = './ep_images'
    if not os.path.exists(config_path):
        print('Could not find the config file.')
        os.system('pause')
        return
    if not os.path.exists(image_path):
        print('Could not find the image path.')
        os.system('pause')
        return
    if not os.path.exists(save_path):
        print('Could not find the save path, created one.')
        os.makedirs(save_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    i_num = config.getint('image','num')
    for dirpath, dirnames, filenames in os.walk(image_path):
        for filename in filenames:
            fpath = os.path.join(dirpath,filename)
            i_num += 1
            current_path = save_path + '/%s%s' % (i_num,os.path.splitext(fpath)[1])
            shutil.move(fpath,current_path)
            print(fpath + '\t-->\t' + current_path)
        if not os.listdir(dirpath) and dirpath != image_path:
            os.rmdir(dirpath)
            print('removed %s' % dirpath)
    config.set('image','num',str(i_num))
    with open(config_path,'w') as cf:
        config.write(cf)
    os.system('pause')

if __name__ == '__main__':
    move_from_excellent_to_ep()