import numpy as np
from PIL import ImageFile
from PIL import Image as pImage
import math
import os, shutil

#responsible for rearranging and image directory to follow the structure#

def rearrange_data(original_data_path, # directory where the images are originally stored
                   new_images_path,     # directory where to store the numpy arrays
                   class_size_limit=None, # optional argument = if specified limits the number of images loaded per class, if this number is higher than the size of some classes, in that class only the number of available files is loaded
                   data_split = 0.9):      #percentage between 0 and 1 of images to store in the train array
    if class_size_limit is not None and class_size_limit < 0:
        raise ValueError("class_size_limit must be > 0")

    classes = []
    total_number_of_files = 0
    for root, dirs, files in os.walk(original_data_path):
        classes += dirs
        if class_size_limit is not None:
            total_number_of_files += min(class_size_limit, len(files)) # número de ficheiros no seu total
        else:
            total_number_of_files += len(files)

    try:
        os.mkdir(new_images_path) # creates the directory where to store the images
    except FileExistsError:
        pass

    #creates the train and test directory
    train_path = os.path.join(new_images_path, "train")
    try:
        os.mkdir(train_path)
    except FileExistsError:
        pass

    test_path = os.path.join(new_images_path, "test")
    try:
        os.mkdir(test_path)
    except FileExistsError:
        pass

    total_count =0 #How many images have already been processes
    for image_class in classes:
        #creates the directory for the class inside the train and test directories
        new_image_class_train_path = os.path.join(train_path,image_class) # test/image_class
        try:
            os.mkdir(new_image_class_train_path)
        except FileExistsError:
            pass

        new_image_class_test_path = os.path.join(test_path,image_class)
        try:
            os.mkdir(new_image_class_test_path)
        except FileExistsError:
            pass

        #counts how many images there are inside each directory and splits it according to the argument given
        original_image_class_path = os.path.join(original_data_path, image_class) # path where the images of a given class were stored
        number_of_images = len(os.listdir(original_image_class_path)) # how many images are there

        if class_size_limit is not None:
            number_of_images = min(class_size_limit, number_of_images) # because of the optional limit

        train_size = math.ceil(number_of_images*data_split) # splits the train and test numbers according to the given argument
        test_size = number_of_images-train_size

        number_of_copied_images_by_style = 0
        train_count =0
        test_count =0
        for img_name in os.listdir(original_image_class_path):
            if number_of_copied_images_by_style== number_of_images: break;

            number_of_copied_images_by_style = number_of_copied_images_by_style + 1
            total_count = total_count + 1

            if number_of_copied_images_by_style  <= train_size :
                shutil.copy(os.path.join(original_image_class_path,img_name), new_image_class_train_path)
                print("class: ", image_class, " Train (",train_count ,"/", train_size, ")",
                      "  Test (0/", test_size,")   TOTAL (",total_count,"/",total_number_of_files,")")
                train_count += 1
            else:
                shutil.copy(os.path.join(original_image_class_path, img_name), new_image_class_test_path)
                print("class: ", image_class, "  Train (", train_count, "/", train_size, ")",
                      "  Test (",test_count,"/", test_size, ")   TOTAL (", total_count, "/",total_number_of_files , ")")
                test_count+=1


