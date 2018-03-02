import os,shutil

def move(frompath,topath,order = False,specialext = ""):
    i_num = 0
    filenames = os.listdir(frompath)
    for filename in filenames:
        fpath = os.path.join(frompath,filename)
        if os.path.isdir(fpath):
            continue

        extname = os.path.splitext(filename)[1]
        if specialext != "" and extname == specialext:
            continue

        if order:
            i_num += 1
            newname = topath + r'\%s%s' % (i_num,extname)
        else:
            newname = os.path.join(topath,filename)

        shutil.move(fpath,newname)
        print(fpath + '\t-->\t' + newname)

def batch_rename_order():
    cpath = os.getcwd()
    cpath += r"\ep_images"
    temppath = cpath+r"\temp"
    
    if not os.path.exists(temppath):
        os.mkdir(temppath)
    
    move(cpath,temppath,True,".py")
    move(temppath,cpath)
    
    if os.path.exists(temppath):
        os.rmdir(temppath)
    
    os.system('pause')

if __name__ == '__main__':
    batch_rename_order()
