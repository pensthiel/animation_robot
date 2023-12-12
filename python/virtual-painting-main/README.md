# **Virtual Painting**

This project is a real-time object detection application that uses OpenCV library to detect and track blue and yellow objects in a video stream. In other words, *Virtual Painting* is a Python project that allows you to draw on your screen with colored markers. 
<br >

## **Requirements**

- Python 3.6 or higher

- OpenCV 4.5.3 or higher

- Numpy 1.19.3 or higher

<br >

## **Installation**

You can install the required packages using pip:
```
pip install -r requirements.txt
```
<br >

## **Usage**

To run the program, open a terminal window and navigate to the directory where you have saved the main.py file, then type:
```
python main.py
```
This will start the video stream and the program will start detecting and tracking blue and yellow objects in real-time. Press '**q**' to quit the program or '**c**' to clean the markers.

<br >

## **Customization**

The colors to detect are represented in the HSV (Hue-Saturation-Value) color space, which is often used in computer vision for color detection. The colors to draw, on the other hand, are represented in the RGB (Red-Green-Blue) color space, which is more commonly used in computer graphics and display systems.

In order to display the detected colors on the screen, we convert the detected colors from the HSV color space to the BGR color space (which is used by OpenCV to represent colors in images and video) and then to RGB. The colors are then displayed on the screen using the RGB color space.

```
# HSV
colors_to_detect = [ 
    # BLUE
   [ 80, 167, 0, 132, 255, 255],
    # YELLOW
    [24,86, 194, 65, 234, 255]
]
```

```
# BGR
colors_to_draw = [
    # BLUE
    (255, 0, 0),
    # YELLOW
    (0, 255, 255)
]
```



If you want to add more colors to the object detection, you can edit the colors list in the **main.py** file. Each color for detecting is defined as a list of six integers: `[H_min, S_min, V_min, H_max, S_max, V_max]`, which represent the minimum and maximum values for the `Hue`, `Saturation`, and `Value` (**HSV**) color space. Each color for drawing is defined as a tuple of three integers: `(Blue, Green, Red)` (**BGR**) color space.  You can find the appropriate values for **colors_to_detect** using range_detector.py and experimenting with different values on the *TrackBars*. Also you can find the appropriate values for your desired **colors_to_draw** easily, just Google it. (and don't forget, it should be in **BGR** form)

The order of the tuples in the **colors_to_draw** must match the order of the colors in **colors_to_detect**, so that the correct color is drawn on each point.




<br >

## **Contributions**

If you are interested in contributing to this project, I welcome your contributions! Feel free to fork the repository and submit pull requests with your changes.

### **Feature Requests**

If you have any ideas for features that could be added to this virtual painting project, please don't hesitate to create an issue on GitHub with the label "feature request". Some possible features that could be added include:

- An eraser tool for removing specific portions of the drawing

- A thicker brush option for bolder lines

- The ability to choose different colors from a color palette

- Saving and loading images

- The ability to export the drawing as an image file

### **Reporting Bugs**

If you come across any bugs or issues while using the virtual painting project, please report them by creating an issue on GitHub with the label "bug". Be sure to include as much detail as possible about what you were doing when the issue occurred and any error messages that were displayed.

Thank you for your interest in contributing to this project!


<br >

## **License**

This dataset is released under the MIT License. Feel free to use it for any purpose, commercial or non-commercial. If you use this dataset, we would appreciate it if you could provide a link back to this repository.

<br >
<br >

**Author: amyrmahdy**

**Date: 13 March 2023** 