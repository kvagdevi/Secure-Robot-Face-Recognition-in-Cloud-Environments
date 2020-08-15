import imageio
import numpy as np
import os
from datetime import datetime
import glob
import cv2
from PIL import Image #importing PIL to read all kind of images
import time
#---------------Read Image to Encrypt---------------
string = 's'
num = 0
start_time = time.time()
list2 = []
for test in string:
    if num == 0:
        filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\att_faces\*'
        savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\hILL CYPHER/'
    if num != 0:
            filepath = r'C:\Users\OEM\Desktop\chiru\colorferet\colorferet\dvd2\gray_feret_cd1\test\inp'
            savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Hill-Cypher---Image-Encryption-master\Images\colorfet databace\Test_encrypted/'
    folders = glob.glob(filepath)
    imagenames = []
    for folder in folders:
        i = 1
        for image in glob.glob(folder + '/*.jpg'):
            imagenames.append(image)

    #read_images = []

    #for image in imagenames:
        #read_images.append(cv2.imread(image, cv2.IMREAD_GRAYSCALE))

    #for face_images in glob.glob(read_images.append):  # assuming jpg
            face_image = Image.open(image)
            if num == 0:
                img = imageio.imread(image)
            if num == 0:
                #img = face_image.convert('RGB')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            l = img.shape[0]
            w = img.shape[1]
            n = max(l,w)
            if n%2:
                n = n + 1
            img2 = np.zeros((n,n,3))
            img2[:l,:w,:] += img                                            #Making the picture to have square dimensions

            #-------------Generating Encryption Key-------------
            Mod = 256
            k = 23                                                          #Key for Encryption

            d = np.random.randint(256, size = (int(n/2),int(n/2)))          #Arbitrary Matrix, should be saved as Key also
            I = np.identity(int(n/2))
            a = np.mod(-d,Mod)

            b = np.mod((k * np.mod(I - a,Mod)),Mod)
            k = np.mod(np.power(k,127),Mod)
            c = np.mod((I + a),Mod)
            c = np.mod(c * k, Mod)

            A1 = np.concatenate((a,b), axis = 1)
            A2 = np.concatenate((c,d), axis = 1)
            A = np.concatenate((A1,A2), axis = 0)
            Test = np.mod(np.matmul(np.mod(A,Mod),np.mod(A,Mod)),Mod)       #making sure that A is an involutory matrix, A*A = I

            # Saving key as an image
            key = np.zeros((n + 1, n))
            key[:n, :n] += A
            # Adding the dimension of the original image within the key
            # Elements of the matrix should be below 256
            key[-1][0] = int(l / Mod)
            key[-1][1] = l % Mod
            key[-1][2] = int(w / Mod)
            key[-1][3] = w % Mod
            imageio.imwrite("Key.png", key)

            #-------------Encrypting-------------
            Enc1 = (np.matmul(A % Mod,img2[:,:,0] % Mod)) % Mod
            Enc2 = (np.matmul(A % Mod,img2[:,:,1] % Mod)) % Mod
            Enc3 = (np.matmul(A % Mod,img2[:,:,2] % Mod)) % Mod

            Enc1 = np.resize(Enc1,(Enc1.shape[0],Enc1.shape[1],1))
            Enc2 = np.resize(Enc2,(Enc2.shape[0],Enc2.shape[1],1))
            Enc3 = np.resize(Enc3,(Enc3.shape[0],Enc3.shape[1],1))
            Enc = np.concatenate((Enc1,Enc2,Enc3), axis = 2)                #Enc = A * image
            iname = image
            src_fname, ext = os.path.splitext(iname)  # split filename and extension
            # construct output filename, basename to remove input directory
            basename = os.path.splitext(os.path.basename(iname))[0]
            imageio.imwrite('Encrypted.png',Enc)
            now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
            rc_fname, ext = os.path.splitext(image)  # split filename and extension
            # construct output filename, basename to remove input directory
            folderbasename = os.path.splitext(os.path.basename(folder))[0]
            basename = os.path.splitext(os.path.basename(image))[0]
            now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
            # byte_array = byte_array
            # filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Train_encrypted/'
            file_path = os.path.join(savepath, folderbasename + "/")
            # file_path = string.join(savepath, "/")
            if i == 1:
                os.makedirs(file_path)
            # cv2.imwrite(file_path + basename + '.jpg', byte_array)
            filename = image
            savepathh = file_path
            imageio.imwrite(savepathh + basename + '.jpg', Enc)
            #save_image(savepath + basename + '.jpg', Enc)
            print("HEXAGEEKS")
            i = 1 + i
            list2.append(time.time() - start_time)
    print("--- %s seconds ---" % (time.time() - start_time))
    avg = (sum(list2)) / max(len(list2), 1)
    print("Average executation time =", avg, "%")
    stdd = np.std(list2)
    print("standerad devation of executation time =", stdd, "%")

    num = num+1

