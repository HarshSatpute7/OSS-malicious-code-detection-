import os
from matplotlib import pyplot as plt
import math
import numpy as np
from PIL import Image
import base64

def convertAndSave(array,name):
    print("X")
    print('Processing '+name)
    if array.shape[1]!=16: #If not hexadecimal
        assert(False)

    b=int( (array.shape[0]*16)*(0.5) )
    b=2**(int(math.log(b)/math.log(2))+1)
    a=int(array.shape[0]*16/b)
    array=array[:a*b//16,:]
    array=np.reshape(array,(a,b))
    im = Image.fromarray(np.uint8(array))
    im.save(root+'\\'+name+'.png', "PNG")
    return im

root = "F:\Coding compe\Flipkart 4.0\Code\Code"
#Get the list of files
files=os.listdir(root)
print('files : ',files)
#We will process files one by one.
for counter, name in enumerate(files):
    #We only process .bytes files from our folder.
    '''
    To convert any file to byte format
    file_path= root+'/'+name
    with open(file_path) as f:
        encoded = base64.b64encode(f.readlines())
    '''
    
    if '.bytes' != name[-6:]:
        continue
    f=open(root+'/'+name)
    array=[]
    for line in f:
        xx=line.split()
        if len(xx)!=17:
            continue
        array.append([int(i,16) if i!='??' else 0 for i in xx[1:] ])
    plt.imshow(convertAndSave(np.array(array),name))
    del array
    f.close()