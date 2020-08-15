import cv2
import numpy as np
from time import time
import math
import csv
from skimage.measure import compare_ssim
import os
import glob
from PIL import Image  # importing PIL to read all kind of images
from datetime import datetime


def ssim(imagename):
    # image='/home/nandinia/Desktop/projects/IAS_proj/image_encryption/image/'+imagename
    image = imagename
    testimage = read_Image(imagename)
    # cv2.imread(image,0)
    output_encrypted = '/home/socialab/Desktop/untitled/Work/Image-Encryption-using-Genetic-Algorithms-Matrix-Manipulation-and-Chaos-Mapping-master/output_GA.jpg'
    encrypted_image = read_Image(output_encrypted)  # cv2.imread(r'',0)

    output_final = '/home/socialab/Desktop/untitled/Work/Image-Encryption-using-Genetic-Algorithms-Matrix-Manipulation-and-Chaos-Mapping-master/output_GA.jpg'
    decrypted_image = read_Image(output_final)
    # cv2.imread(r'output_final.jpg',0)
    ssim1 = compare_ssim(testimage, encrypted_image)
    ssim2 = compare_ssim(testimage, decrypted_image)
    print("image and encrypted", ssim1)
    print("image and decrypted", ssim2)

    return ssim1, ssim2


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
    # coiter=(9*x+8*y)%l
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
    # muiter=(76*x+93*y)%l
    muiter = (5 * x + 73 * y) % l
    # print("muiter",muiter)

    for j in range(0, muiter):
        n1 = number_gen(mui, j, l)
        # print("number",n1)
        vector[n1] = 255 - vector[n1]
    return vector


def rotate_Matrix_90(Matrix):
    N = len(Matrix)
    for x in range(0, int(N / 2)):

        for y in range(x, N - x - 1):
            # store current cell in temp variable
            temp = Matrix[x][y]
            Matrix[x][y] = Matrix[y][N - 1 - x]
            Matrix[y][N - 1 - x] = Matrix[N - 1 - x][N - 1 - y]
            Matrix[N - 1 - x][N - 1 - y] = Matrix[N - 1 - y][x]
            Matrix[N - 1 - y][x] = temp
    return Matrix


# Function to print the Matrix
def printMatrix(Matrix):
    N = len(Matrix[0])
    for i in range(N):
        print(Matrix[i])


def reshape(Matrix):
    n = int(math.sqrt(len(Matrix)))
    Matrix = np.array(Matrix).reshape((n, n))
    return Matrix


def rotate_Matrix_180(Matrix):
    rotate = rotate_Matrix_90(Matrix)
    rotate = rotate_Matrix_90(rotate)
    return rotate


def rotate_Matrix_270(Matrix):
    rotate = rotate_Matrix_90(Matrix)
    rotate = rotate_Matrix_90(rotate)
    rotate = rotate_Matrix_90(rotate)
    return rotate


def slice_Matrix(Matrix):
    slice1 = []
    slice2 = []
    slice3 = []
    slice4 = []
    slice5 = []
    slice6 = []
    slice7 = []
    slice8 = []
    Slice = []

    for row in Matrix:
        for item in row:
            slice1.append(item[0])
            slice2.append(item[1])
            slice3.append(item[2])
            slice4.append(item[3])
            slice5.append(item[4])
            slice6.append(item[5])
            slice7.append(item[6])
            slice8.append(item[7])

    slice1 = reshape(slice1)
    Slice.append(slice1)
    slice2 = reshape(slice2)
    Slice.append(slice2)
    slice3 = reshape(slice3)
    Slice.append(slice3)
    slice4 = reshape(slice4)
    Slice.append(slice4)
    slice5 = reshape(slice5)
    Slice.append(slice5)
    slice6 = reshape(slice6)
    Slice.append(slice6)
    slice7 = reshape(slice7)
    Slice.append(slice7)
    slice8 = reshape(slice8)
    Slice.append(slice8)
    return Slice


def encrpyt_bit_rotation(Matrix):
    for i in range(len(Matrix)):
        if i in [0, 3, 6]:
            rotate90 = rotate_Matrix_90(Matrix[i])
            Matrix[i] = rotate90
        elif i in [1, 4, 7]:
            rotate180 = rotate_Matrix_180(Matrix[i])
            Matrix[i] = rotate180
        elif i in [2, 5]:
            rotate270 = rotate_Matrix_270(Matrix[i])
            Matrix[i] = rotate270
    return Matrix


def decrpyt_bit_rotation(Matrix):
    for i in range(len(Matrix)):
        if i in [0, 3, 6]:
            rotate90 = rotate_Matrix_270(Matrix[i])
            Matrix[i] = rotate90
        elif i in [1, 4, 7]:
            rotate180 = rotate_Matrix_180(Matrix[i])
            Matrix[i] = rotate180
        elif i in [2, 5]:
            rotate270 = rotate_Matrix_90(Matrix[i])
            Matrix[i] = rotate270
    return Matrix


def join_bit(Matrix):
    Matrix = np.array(Matrix)
    no_of_slices = Matrix.shape[0]
    rows_of_each_slice = Matrix.shape[1]

    joined_bits = []
    for i in range(rows_of_each_slice):
        bit_array = []
        for j in range(rows_of_each_slice):
            pixel = ''
            for slices in range(no_of_slices):
                pixel += Matrix[slices, i][j]
            # bit_array.append(pixel)
            bit_array.append(int(pixel, 2))
        joined_bits.append(bit_array)
    # print(joined_bits)
    return joined_bits


def bit_slice_encrypt(Array):
    rows = Array.shape[0]
    cols = Array.shape[1]
    bin_Array = []
    for i in range(rows):
        subset = []
        for j in range(cols):
            subset.append(bin(Array[i, j])[2:].zfill(8))
        bin_Array.append(subset)
    sliced = np.array(slice_Matrix(bin_Array))
    encrpyt_rotated = encrpyt_bit_rotation(sliced)
    bit = join_bit(encrpyt_rotated)
    bit = np.array(bit)
    return bit


def bit_slice_decrypt(Array):
    rows = Array.shape[0]
    cols = Array.shape[1]
    bin_Array = []
    for i in range(rows):
        subset = []
        for j in range(cols):
            subset.append(bin(Array[i, j])[2:].zfill(8))
        bin_Array.append(subset)
    sliced = np.array(slice_Matrix(bin_Array))
    decrpyt_rotated = decrpyt_bit_rotation(sliced)
    bit = join_bit(decrpyt_rotated)
    bit = np.array(bit)
    return bit


def Algorithm_encrypt(bitarray):
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
        vectors[i] = crossover(vectors[i], r1, r2, l)
        vectors[i] = mutate(vectors[i], r1, r2, l)
        r1 += 1
        r2 += 1

    crypt = np.zeros((height, width))
    count = 0

    for i in range(0, len(crypt)):
        dummy = np.append([], vectors[count * frags_per_row:(count + 1) * frags_per_row])
        count += 1
        crypt[i] = dummy
    crypt = crypt.astype(int)
    # print("before encrypt rotate",crypt)
    crypt = bit_slice_encrypt(crypt)
    # print("after encrypt rotate=",crypt)
    return crypt


def Algorithm_decrypt(bitarray):
    # bitarray=cv2.imread(image,0)
    # bitarray=cv2.resize(bitarray,(256,256))
    # print("befpre decrypt rotate",bitarray)
    bitarray = bit_slice_decrypt(bitarray)
    # print("after decrypt rotate=",bitarray)

    width = len(bitarray[0])
    height = len(bitarray)

    fragments = 1
    frags_per_row = 1
    l = width // fragments

    r1, r2 = Get_r_values(width, height, l, bitarray)
    vectors = createvectors(bitarray, l)

    for i in range(0, len(vectors)):
        vectors[i] = crossover(vectors[i], r1, r2, l)
        vectors[i] = mutate(vectors[i], r1, r2, l)
        r1 += 1
        r2 += 1

    crypt = np.zeros((height, width))
    count = 0

    for i in range(0, len(crypt)):
        dummy = np.append([], vectors[count * frags_per_row:(count + 1) * frags_per_row])
        count += 1
        crypt[i] = dummy
    crypt = crypt.astype(int)

    # print("bits converted to image=",crypt)
    return crypt


def createImage(filename, byte_array, savepath, imagename):
    src_fname, ext = os.path.splitext(imagename)  # split filename and extension
    # construct output filename, basename to remove input directory
    basename = os.path.splitext(os.path.basename(imagename))[0]
    now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    # filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\bit_and_algo_Images\Train_encrypted/'
    cv2.imwrite(savepath + basename + '.jpg', byte_array)
    # cv2.imwrite(filename,byte_array)
    print("Image created!")


def read_Image(imagename):
    # image='/home/nandinia/Desktop/projects/IAS_proj/image_encryption/image/'+imagename
    image = imagename
    print(image)
    bitarray = cv2.imread(image, 0)
    bitarray = cv2.resize(bitarray, (256, 256))
    return bitarray


def Algorithm_file(imagename, savepath):
    bitarray = read_Image(imagename)
    t1 = time()
    print("Encrypting image...")
    # encrypted array
    byte_array = Algorithm_encrypt(bitarray)
    print("Creating Encrypted image..")
    output = "output_encrypted.jpg"
    createImage(output, byte_array, savepath, imagename)
    t2 = time()
    encrypttime = t2 - t1
    # print("Time taken to encrypt:",encrypttime)
    t1 = time()
    print("Decrypting image...")
    byte_array2 = Algorithm_decrypt(byte_array)
    print("Creating Decrypted image..")
    output = "output_final.jpg"
    # 77createImage(output,byte_array2)
    t2 = time()
    decrypttime = t2 - t1
    # ssim1=compare_ssim(np.array(bitarray),np.array(byte_array))
    # ssim2=compare_ssim(np.array(bitarray),np.array(byte_array2))
    # print("Time taken to decrypt:",decrypttime)
    # ssim1,ssim2=ssim(imagename)

    return imagename, encrypttime, decrypttime  # ,ssim1,ssim2


def Algorith_image(imagename):
    bitarray = read_Image(imagename)
    t1 = time()
    print("Encrypting image...")
    # encrypted array
    byte_array = Algorithm_encrypt(bitarray)
    print("Creating Encrypted image..")
    output = "output_encrypted.jpg"
    createImage(output, byte_array)
    t2 = time()
    encrypttime = t2 - t1
    print("Time taken to encrypt:", encrypttime)
    t1 = time()
    # image=input("Enter name of image to be decrypted:")
    print("Decrypting image...")
    byte_array2 = Algorithm_decrypt(byte_array)
    print("Creating Decrypted image..")
    output = "output_final.jpg"
    createImage(output, byte_array2)
    t2 = time()
    decrypttime = t2 - t1
    print("Time taken to decrypt:", decrypttime)


def main():
    # lines = csv.reader(open('/home/nandinia/Desktop/projects/IAS_proj/image_encryption/image/image.csv', "r"))
    # dataset = list(lines)
    # print(dataset)
    analysis = []
    #start_time = time.time()
    list2 = []
    string = 's'
    num = 0
    for test in string:
        if num == 0:
            filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\att_faces\*'
            savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\BIT SLICE/'
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
                for imagename in glob.glob(folder + '/*.jpg'):  # assuming jpg
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
                    # cv2.imwrite(file_path + basename + '.jpg', byte_array)
                    # imagename = Image.open(imagename)
                    savepathh = file_path
                    imagename, encrypttime, decrypttime = Algorithm_file(imagename, savepathh)
                    # subset.append(imagename)
                    print("encrypttime", encrypttime)
                    # subset.append(encrypttime)
                    # subset.append(ssim_e)
                    print("decrypttime", decrypttime)
                    i = 1 + i
                    list2.append(encrypttime)
    print("--- %s seconds ---" % (encrypttime))
    avg = (sum(list2)) / max(len(list2), 1)
    print("Average executation time =", avg, "%")
    stdd = np.std(list2)
    print("standerad devation of executation time =", stdd, "%")
                    # subset.append(decrypttime)
                    # subset.append(ssim_d)
                    # analysis.append(subset)
    # with open('image_analysis.csv', mode='w') as employee_file:
    # employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # for item in analysis:
    # employee_writer.writerow(item)
    '''
    imagename=input("enter the name:")
    print(imagename)
    Algorith_image(imagename)
'''


if __name__ == '__main__':
    main()

