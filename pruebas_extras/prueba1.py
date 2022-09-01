# -*- coding: utf-8 -*-
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage import exposure
import matplotlib.pyplot as plt
import dlib
from skimage import io
import face_recognition_models
import numpy as np


# reading the image
img = imread('team1.jpg')
plt.figure()
plt.axis("off")
plt.imshow(img)
print(img.shape)

# resizing image
resized_img = resize(img, (128*4, 64*4))
plt.figure()
plt.axis("off")
plt.imshow(resized_img)
print(resized_img.shape)

#creating hog features
fd, hog_image = hog(resized_img, orientations=9, pixels_per_cell=(8, 8),
                	cells_per_block=(2, 2), visualize=True, multichannel=True)
plt.figure()
plt.axis("off")
plt.imshow(hog_image, cmap="gray")

# tomamos una imagen
file_name = 'team1.jpg'

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()
print(face_detector)

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
face_pose_predictor =dlib.shape_predictor(predictor_68_point_model)

print(face_pose_predictor)

face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

win = dlib.image_window()

# Load the image into an array
image = io.imread(file_name)

# Run the HOG face detector on the image data.
# The result will be the bounding boxes of the faces in our image.
detected_faces = face_detector(image, 1)    
print(detected_faces)
print(type(detected_faces))

print("I found {} faces in the file {}".format(len(detected_faces), file_name))

# Open a window on the desktop showing the image
win.set_image(image)

# Loop through each face we found in the image
for i, face_rect in enumerate(detected_faces):
    #face_image = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
    #pil_image = Image.fromarray(face_image)
    #pil_image.show()
	# Detected faces are returned as an object with the coordinates 
	# of the top, left, right and bottom edges
    print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

	# Draw a box around each face we found
    win.add_overlay(face_rect)
    
    # Get the the face's pose
    pose_landmarks = face_pose_predictor(image, face_rect)
    
    
	# Draw the face landmarks on the screen.
    win.add_overlay(pose_landmarks)
    # se obtiene el descriptor cada rostro 
    face_descriptor = face_encoder.compute_face_descriptor(image, pose_landmarks)
    print(face_descriptor)
    print(type(face_encoder))
	        
# Wait until the user hits <enter> to close the window	        
dlib.hit_enter_to_continue()
