from auto_drive_functions import retrieve_angle 
from PIL import Image, ImageShow
from ImageFrame import Frame
import matplotlib.pyplot as plt
import timeit as ti
import numpy as np


def debugging(img, angle, points=None, mid_points=None):
    print("======================== Debug Mode ==============================")
    print(type(img))
    width, height =[640,480]
    
    start_time = ti.default_timer()
    end_time = ti.default_timer()

    print("Start:", start_time)
    print("End:", end_time)
    print("Runtime: ", end_time - start_time)


    plt.axis([0.0, width, 0.0, height])
    img_as_np = np.array(img)

    # Change color of Image
    img_as_np = img_as_np[:,:,0]

    # Show Changed Image as Background
    plt.imshow(img_as_np)

    # Plot points as red dot
    for x, y in points:
        plt.plot(x, y, 'ro')
    
    for x, y, a in mid_points:
        plt.plot(x, y, 'b^')

    # Save figure to file
    plt.savefig("foo.png", format='png')

    # Display Image from file
    new_img = Image.open("foo.png")
    ImageShow.show(new_img)