import cv2
from math import sin,pi,floor
import numpy as np
from time import time
import os
import glob
from datetime import datetime

def chirikov(x):
    height,width=len(x),len(x[0])
    n=height
    K=10000000 #this parameter acts as the key.It decides the degree of deviation in the image
    newarray=np.zeros((height,width))
    newarray[0][0]=x[0][0]
    for i in range(height):
        for j in range(width):
            if (i+j)!=0:
                xnew=(i-1+j-1)%n
                ynew=(floor(j-1+K*sin(2*pi*xnew/n)))%n
                newarray[xnew][ynew]=x[i][j]
    for i in range(height):
        for j in range(width):
            x[i][j]=newarray[i][j]
    return x

def chirikovdec(x): #the decryption function
    height,width=len(x),len(x[0])
    n=height
    K=10000000#this parameter has to be equal to its counterpart in the encrypt function.
    newarray=np.zeros((height,width))
    newarray[0][0]=x[0][0]
    for i in range(height):
        for j in range(width):
            if (i+j)!=0:
                xnew=(floor(i-j+K*sin(2*pi*(i)/n)))%n
                ynew=(floor(j-K*sin(2*pi*(i)/n)))%n
                newarray[xnew][ynew]=x[i][j]
    for i in range(height):
        for j in range(width):
            x[i][j]=newarray[i][j]
    return x


if __name__=="__main__":
    string = 's'
    num = 0
    for test in string:
        if num == 0:
            filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\att_faces\*'
            savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\Chaos/'
        if num != 0:
            filepath = r'C:\Users\OEM\Desktop\chiru\colorferet\colorferet\dvd2\gray_feret_cd1\test\inp\*'
            savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Test_encrypted/'
        #password = hashlib.sha256('2'.encode("UTF-8")).hexdigest()
        # password = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
        if len(os.listdir(savepath)) != 100:
            folders = glob.glob(filepath)
            imagenames = []
            for folder in folders:
                i = 1
                for face_images in glob.glob(folder + '/*.jpg'):  # assuming jpg
                    x=cv2.imread(face_images, 0)
                    x = cv2.resize(x, (int(200), int(200)))
                    t1=time()
                    x=chirikov(x)
                    t2=time()
                    #x=chirikovdec(x)
                    t3=time()
                    print(t2-t1,t3-t2)
                    imagename = face_images
                    src_fname, ext = os.path.splitext(imagename)  # split filename and extension
                    # construct output filename, basename to remove input directory
                    basename = os.path.splitext(os.path.basename(imagename))[0]
                    now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                    #filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-Algorithms-Matrix-Manipulation-and-Chaos-Mapping-master\CryptoChaos_Images\Train_encrypted/'
                    # print("Encrypting image...")
                    # byte_array = Algorithm(imagename)
                    src_fname, ext = os.path.splitext(imagename)  # split filename and extension
                    # construct output filename, basename to remove input directory
                    folderbasename = os.path.splitext(os.path.basename(folder))[0]
                    basename = os.path.splitext(os.path.basename(imagename))[0]
                    now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                    # byte_array = byte_array
                    # filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Train_encrypted/'
                    file_path = os.path.join(savepath, folderbasename + "/")
                    # file_path = string.join(savepath, "/")
                    if i == 1:
                        os.makedirs(file_path)
                    cv2.imwrite(file_path + basename + '.jpg', x)
                    #cv2.imwrite("output_Chaos.jpg",x)
                    #cv2.imwrite("output_Chaos_decrypted.jpg",x)
                    i = 1 + i

        num = num+1
