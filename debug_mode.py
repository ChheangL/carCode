from auto_drive_functions import retrieve_angle 
from PIL import Image, ImageShow
from ImageFrame import Frame
import matplotlib.pyplot as plt
import timeit as ti
import numpy as np


def debugging(img, angle, points=None, mid_points=None):
    print("======================== Debug Mode ==============================")
    width, height = img.size
    
    start_time = ti.default_timer()
    end_time = ti.default_timer()

    print("Start:", start_time)
    print("End:", end_time)
    print("Runtime: ", end_time - start_time)


    plt.axis([0.0, width, 0.0, height])
    img_as_np = np.array(img)

    # Change color of Image
    img_as_np = img_as_np[:,:,2]

    # Show Changed Image as Background
    plt.imshow(img_as_np)

    # Plot points as red dot
    for x, y in points:
        plt.plot(x, y, 'ro')

    # Save figure to file
    plt.savefig("foo", format='png')

    # Display Image from file
    new_img = Image.open("foo.png")
    ImageShow.show(new_img.rotate(angle=180, expand=True))