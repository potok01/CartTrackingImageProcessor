import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sci
import os

def main():
    # Meters per pixel
    meters_per_pixel = 1.6 / 1280

    # Frame rate
    frame_rate = 30

    # File path
    path = "C:\\Users\\apoto\\Desktop\\Test Videos\\"
    img_list_names = sorted(os.listdir(path))
    # Time between frames
    del_t = 1/frame_rate

    # Lists to store position data
    x = [[], [], []]

    # Lists to store velocity data
    v_x = [[], [], []]

    # Lists to store acceleration data
    a_x = [[], [], []]

    propeller_sizes = ["Large","Medium","Small"]
    for i in range(0,len(propeller_sizes)):

        # Get a list of folders for each propeller size
        current_path = path + propeller_sizes[i] + "\\"
        folders = sorted(os.listdir(current_path))

        print(folders)
        # For each folder of frames in each size of propeller, do stuff
        for j in range(0,len(folders)):
            current_folder_path = path + propeller_sizes[i] + "\\" + folders[j] + "\\"
            img_list_names = sorted(os.listdir(current_folder_path))

            # Get images from file
            img_list = []
            for k in range(0, len(img_list_names)):
                img_list.append(cv.imread(current_folder_path + img_list_names[k]))

            # Lists to store x and y position
            x_temp = []
            y_temp = []
            for k in range(0,len(img_list)):
                # Get image from list
                img = img_list[k]

                # Crop image
                img = img[750:900, :]

                # Convert image to hue luminosity saturation colorspace
                img = cv.cvtColor(img, cv.COLOR_BGR2HLS)

                # Set lower and upper limits on luminosity
                lower_luminosity = np.array([0,8,0])
                upper_luminosity = np.array([255,255,255])

                # Create a mask of only the pixels that are within the above defined thresholds
                mask = cv.inRange(img, lower_luminosity, upper_luminosity)

                # Create a kernel to erode and then dilate mask
                kernel = np.ones((10, 10), np.uint8)
                mask = cv.erode(mask, kernel, iterations=1)
                mask = cv.dilate(mask, kernel, iterations=1)

                # Use the above mask to extract only the retro-reflective marker from the image
                img = cv.bitwise_and(img, img, mask=mask)

                # Convert the image to the greyscale colorspace
                img = cv.cvtColor(img, cv.COLOR_HLS2BGR)
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # Find the contours from the image, should only be the rectangle of the tape
                contours, hierarchy = cv.findContours(img, 1, 2)
                cv.drawContours(img, contours, -1, (100,127,0), 2)

                img_list[k] = img

                try:
                    cnt = contours[0]
                    moments = cv.moments(cnt)
                    x_temp.append((int(moments['m10'] / moments['m00'])) * meters_per_pixel)
                    y_temp.append((int(moments['m01'] / moments['m00'])) * meters_per_pixel)
                except IndexError:
                    x_temp.append(0)
                    y_temp.append(0)


            # Lists to hold velocities
            v_x_temp = [0]
            v_y_temp = [0]

            # Calculate the velocity as change in displacement over change in time
            for k in range(1, len(x_temp)):
                v_x_temp.append((x_temp[k] - x_temp[k-1])/(del_t))
                v_y_temp.append((y_temp[k] - y_temp[k-1])/(del_t))

            # Lists to hold accelerations
            a_x_temp = [0]
            a_y_temp = [0]

            # Calculate the acceleration as change in velocity over change in time
            for k in range(1, len(x_temp)):
                a_x_temp.append((v_x_temp[k] - v_x_temp[k-1])/(del_t))
                a_y_temp.append((v_y_temp[k] - v_y_temp[k-1])/(del_t))

            x[i].append(x_temp[1:])
            v_x[i].append(v_x_temp[1:])
            a_x[i].append(a_x_temp[1:])
            print(j)

            # if j == 6:
            #     for k in range(0,len(img_list)):
            #         cv.imshow(str(k), img_list[k])
            #         print(v_x_temp[k])
            #         k = cv.waitKey(0)

    t = [[],[],[]]


    for i in range(0, len(x)):
        for j in range(0, len(x[i])):
            temp = []
            for k in range(0, len(x[i][j])):
                temp.append(k*del_t)
            t[i].append(temp)

    print("t = ",end='')
    print(t)
    print("x = ",end='')
    print(x)
    print("v_x = ",end='')
    print(v_x)
    print("a_x = ",end='')
    print(a_x)
    # plt.legend(loc="upper left")
    plt.show()








main()