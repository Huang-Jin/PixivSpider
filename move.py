import os,shutil

def move_from_excellent_to_ep():
    image_path = './original_images/excellent'
    save_path = './ep_images'
    if not os.path.exists(image_path):
        print('Could not find the image path.')
        os.system('pause')
        return
    if not os.path.exists(save_path):
        print('Could not find the save path, created one.')
        os.makedirs(save_path)
    for dirpath, dirnames, filenames in os.walk(image_path):
        for filename in filenames:
            fpath = os.path.join(dirpath,filename)
            current_path = os.path.join(save_path,dirpath[-8:] + '-' + filename)
            shutil.move(fpath,current_path)
            print(fpath + '\t-->\t' + current_path)
        if not os.listdir(dirpath) and dirpath != image_path:
            os.rmdir(dirpath)
            print('removed %s' % dirpath)
    os.system('pause')

if __name__ == '__main__':
    move_from_excellent_to_ep()