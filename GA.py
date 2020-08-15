import cv2
import numpy as np
from time import time
from PIL import Image  # importing PIL to read all kind of images
import os
import glob
from datetime import datetime
import numpy as np  # importing numpy
from PIL import Image  # importing PIL to read all kind of images


def Get_r_values(width, height, l, image):
    R1, R11 = 0, 0
    R2, R22 = 0, 0
    for i in range(width - 1):
        for j in range(height - 1):
            a = pow(-1, (i + j)) * image[i][j]
            b = pow(-1, (i + j + 1)) * image[i][j]
            R11 = R11 + a
            R22 = R22 + b
            # print(R1
    R1 = abs(R11 // width * l)
    R2 = abs(R22 // height * l)
    print('r1:', R1, 'r2:', R2)
    return R1, R2


def number_gen(seed, iters, l):
    op = seed
    while iters:
        op = (29 * seed + 13) % l
        seed = op
        iters -= 1
    return op


def createvectors(x, l):
    frags_per_row = len(x[0]) // l
    # print(frags_per_row)
    vectors = []
    for dummyvectors in x:
        for i in range(0, frags_per_row):
            vectors.append(dummyvectors[i * l:(i + 1) * l])
    return vectors


def crossover(vector, x, y, l):
    if x < l and y < l:
        coi = x
    else:
        coi = 0
    coiter = (3 * x + 5 * y) % l

    for j in range(0, 2 * coiter, 2):
        n1 = number_gen(coi, j, l)
        n2 = number_gen(coi, j + 1, l)
        temp = vector[n1]
        vector[n1] = vector[n2]
        vector[n2] = temp
    return vector


def mutate(vector, x, y, l):
    if x < l and y < l:
        mui = y
    else:
        mui = 0
    muiter = (5 * x + 73 * y) % l
    # print("muiter",muiter)

    for j in range(0, muiter):
        n1 = number_gen(mui, j, l)
        # print("number",n1)
        vector[n1] = 255 - vector[n1]
        # print('vector',vector[n1])
    return vector


def Algorithm(image):
    # image='test.jpg'
    bitarray = cv2.imread(image, 0)
    bitarray = cv2.resize(bitarray, (256, 256))

    width = len(bitarray[0])
    height = len(bitarray)

    fragments = 1
    frags_per_row = 1

    l = width // fragments
    # print("l",l)

    r1, r2 = Get_r_values(width, height, l, bitarray)
    # r1,r2=20,30
    vectors = createvectors(bitarray, l)

    for i in range(0, len(vectors)):
        # print('before',vectors[i])
        vectors[i] = crossover(vectors[i], r1, r2, l)
        # print('after',vectors[i])
        vectors[i] = mutate(vectors[i], r1, r2, l)
        r1 += 1
        r2 += 1

    crypt = np.zeros((height, width))
    # print(crypt.shape)
    count = 0
    # cv2.imwrite("output2_GA.jpg",crypt)
    for i in range(0, len(crypt)):
        dummy = np.append([], vectors[count * frags_per_row:(count + 1) * frags_per_row])
        count += 1
        crypt[i] = dummy
        # print(dummy)
    # crypt.save('/home/socialab/Desktop/untitled/Work/Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master/Images/Train_encrypted/' + now + '.jpg')
    return crypt


def createImage(filename, byte_array):
    cv2.imwrite(filename, byte_array)
    print("Image created!")


if __name__ == "__main__":
    '''
    #image="test.jpg"
    image="output_GA.jpg"
    GA_bytearray=Algorithm(image)
    #output="output_GA.jpg"
    output="final.jpg"
    createImage(output,GA_bytearray)
    '''
    print("1.Encrypt \n2.Decrypt")
    option = int(input("Enter option"))
    imagename = ""
    if option == 1:

        string = 's'
        num = 0
        list2 = []
        for test in string:
            if num == 0:
                filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\att_faces\*'
                savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\GA/'
            if num != 0:
                filepath = r'C:\Users\OEM\Desktop\chiru\colorferet\colorferet\dvd2\gray_feret_cd1\test\inp\*'
                savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Test_encrypted/'
            # password = hashlib.sha256('2'.encode("UTF-8")).hexdigest()
            # password = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
            if len(os.listdir(savepath)) != 1000000:
                folders = glob.glob(filepath)
                imagenames = []
                for folder in folders:
                    i = 1
                    for imagename in glob.glob(folder + '/*.jpg'):  # assuming jpg
                        t1 = time()
                        # print("Encrypting image...")
                        byte_array = Algorithm(imagename)
                        src_fname, ext = os.path.splitext(imagename)  # split filename and extension
                        # construct output filename, basename to remove input directory
                        folderbasename = os.path.splitext(os.path.basename(folder))[0]
                        basename = os.path.splitext(os.path.basename(imagename))[0]
                        now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                        byte_array = byte_array
                        # filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Train_encrypted/'
                        file_path = os.path.join(savepath, folderbasename + "/")
                        #file_path = string.join(savepath, "/")
                        if i == 1:
                           os.makedirs(file_path)
                        cv2.imwrite(file_path + basename + '.jpg', byte_array)
                        print("Creating Encrypted image..")
                        output = "output_e.jpg"
                        createImage(output, byte_array)
                        t2 = time()
                        print("Time taken to encrypt:", t2 - t1)
                        i = i+1
                        list2.append(t2 - t1)
            print("--- %s seconds ---" % (t2 - t1))
            avg = (sum(list2)) / max(len(list2), 1)
            print("Average executation time =", avg, "%")
            stdd = np.std(list2)
            print("standerad devation of executation time =", stdd, "%")

    if option == 2:
        t1 = time()
        image = input("Enter name of image to be decrypted:")
        print("Decrypting image...")
        byte_array = Algorithm(image)
        print("Creating Decrypted image..")
        output = "output_final.jpg"
        createImage(output, byte_array)
        t2 = time()
        print("Time taken to decrypt:", t2 - t1)


