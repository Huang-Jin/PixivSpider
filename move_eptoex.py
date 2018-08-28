import os, shutil
import configparser

def move_from_ep_to_excellent():
    config_path = './config_files/move.cfg'
    save_path = './original_images/excellent'
    image_path = './ep_images'
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

if __name__ == '__main__':
    move_from_ep_to_excellent()