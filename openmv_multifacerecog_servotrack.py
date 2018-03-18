# Face Tracking and Recognition
#
# 2017-2018 AK, The Teddy Robot Project
#
# NOTE: LOTS OF KEYPOINTS MAY CAUSE THE SYSTEM TO RUN OUT OF MEMORY!
#
# servo code not yet migrated to I2C, and object notifications also not finished

import sensor, time, image
#from pyb import I2C
from pyb import LED

#green_led = LED(1)
#blue_led = LED(2)
red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)
ir_leds = LED(4)
#ir_leds.on() # makes only sense when lens is replace with non-ir-cut-filter

#init IIC as master
#i2c = I2C(2, I2C.MASTER) # The i2c bus must always be 2.

# Init Tracking positions
x_pos = 1800 # default
y_pos = 1500 # default
x_error = 0
y_error = 0
x_min = 1400
x_max = 2200
y_max = 1900
y_min = 1100

x_gain = +1.00 # You have to tweak this value to stablize the control loop.
               # You also may need to invert the value if the system goes
               # in the wrong direction.
y_gain = +1.00 # You have to tweak this value to stablize the control loop.
               # You also may need to invert the value if the system goes
               # in the wrong direction.

# Normalized keypoints are not rotation invariant...
NORMALIZED=True
# Keypoint extractor threshold, range from 0 to any number.
# This threshold is used when extracting keypoints, the lower
# the threshold the higher the number of keypoints extracted.
KEYPOINTS_THRESH=3
# Keypoint-level threshold, range from 0 to 100.
# This threshold is used when matching two keypoint descriptors, it's the
# percentage of the distance between two descriptors to the max distance.
# In other words, the minimum matching percentage between 2 keypoints.
MATCHING_THRESH=85

# Number of maximum keypoints
KEYPOINTS_MAX=80



# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface")


# First set of keypoints
leo_kpts = None
andy_kpts = None
taiga_kpts = None
aya_kpts = None

# load faces!
img_andy = image.Image("/andy11.pgm",copy_to_fb=True)
andy_objects = img_andy.find_features(face_cascade, threshold=0.7, scale=1.3)
if andy_objects:
        print("Andy's face loaded!")
        # Expand the ROI by 31 pixels in each direction (half the pattern scale)
        andy_face = (andy_objects[0][0]-31, andy_objects[0][1]-31,andy_objects[0][2]+31*2, andy_objects[0][3]+31*2)
        # Extract keypoints using the detect face size as the ROI
        andy_kpts = img_andy.find_keypoints(threshold=KEYPOINTS_THRESH, scale_factor=1.3, max_keypoints=KEYPOINTS_MAX, normalized=NORMALIZED, roi=andy_face)

# Draw keypoints
print("Andy's key points")
print(andy_kpts)

img_aya = image.Image("/aya11.pgm",copy_to_fb=True)
aya_objects = img_aya.find_features(face_cascade, threshold=0.7, scale=1.0)
if aya_objects:
        print("Aya's face loaded!")
        # Expand the ROI by 31 pixels in each direction (half the pattern scale)
        aya_face = (aya_objects[0][0]-31, aya_objects[0][1]-31,aya_objects[0][2]+31*2, aya_objects[0][3]+31*2)
        # Extract keypoints using the detect face size as the ROI
        aya_kpts = img_aya.find_keypoints(threshold=KEYPOINTS_THRESH, scale_factor=1.3, max_keypoints=KEYPOINTS_MAX, normalized=NORMALIZED, roi=aya_face)

# Draw keypoints
print("Aya's key points")
print(aya_kpts)

img_taiga = image.Image("/taiga12.pgm",copy_to_fb=True)
taiga_objects = img_taiga.find_features(face_cascade, threshold=0.7, scale=1.0)
if taiga_objects:
        print("Taiga's face loaded!")
        # Expand the ROI by 31 pixels in each direction (half the pattern scale)
        taiga_face = (taiga_objects[0][0]-31, taiga_objects[0][1]-31,taiga_objects[0][2]+31*2, taiga_objects[0][3]+31*2)
        # Extract keypoints using the detect face size as the ROI
        taiga_kpts = img_taiga.find_keypoints(threshold=KEYPOINTS_THRESH, scale_factor=1.3, max_keypoints=KEYPOINTS_MAX, normalized=NORMALIZED, roi=taiga_face)

# Draw keypoints
print("Taiga's key points")
print(taiga_kpts)

img_leo = image.Image("/leo12.pgm",copy_to_fb=True)
leo_objects = img_leo.find_features(face_cascade, threshold=0.7, scale=1.0)
if leo_objects:
        print("Leo's face loaded!")
        # Expand the ROI by 31 pixels in each direction (half the pattern scale)
        leo_face = (leo_objects[0][0]-31, leo_objects[0][1]-31,leo_objects[0][2]+31*2, leo_objects[0][3]+31*2)
        # Extract keypoints using the detect face size as the ROI
        leo_kpts = img_leo.find_keypoints(threshold=KEYPOINTS_THRESH, scale_factor=1.3, max_keypoints=KEYPOINTS_MAX, normalized=NORMALIZED, roi=leo_face)

# Draw keypoints
print("Leo's key points")
print(leo_kpts)

# FPS clock
clock = time.clock()
c=[0,0,0,0,0]# 1-4:number of matchpoints for andy,aya,leo,taiga;0:temp value
i=[0,0,0,0,0]# 1-4:times of match for andy,aya,leo,taiga;0:temp value


# Set camera format
sensor.reset()
sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.QVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

bounding_box=0
BOX_MAXAGE=150 # Frames, keep below 255 for substraction from color
box_aging=BOX_MAXAGE
FACE=""

while (True):
    if bounding_box:
      img.draw_rectangle(bounding_box, color=255-box_aging)
      img.draw_string(0, 10, FACE, color=0)
    box_aging=box_aging+1
    if box_aging >= BOX_MAXAGE:
      box_aging=BOX_MAXAGE
      bounding_box=0
    clock.tick()
    img = sensor.snapshot()
    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()),color=0 )
    img_objects = img.find_features(face_cascade, threshold=0.7, scale=1.0)
    if img_objects:
            #print("a new face detected!")
            # Draw a rectangle around the first face
            bounding_box=img_objects[0]
            box_aging=0
            img.draw_rectangle(bounding_box)
            # Expand the ROI by 31 pixels in each direction (half the pattern scale)
            img_face = (img_objects[0][0]-31, img_objects[0][1]-31,img_objects[0][2]+31*2, img_objects[0][3]+31*2)
            # Extract keypoints using the detect face size as the ROI
            kpts = img.find_keypoints(threshold=KEYPOINTS_THRESH, scale_factor=1.0, max_keypoints=KEYPOINTS_MAX, normalized=NORMALIZED, roi=img_face)

            if (kpts):
                #img.draw_keypoints(kpts,size=2,color=0)
                #print("keypoints found!")
                # Match the first set of keypoints with the second one
                c1 = image.match_descriptor(andy_kpts, kpts,threshold=MATCHING_THRESH)
                c2 = image.match_descriptor(aya_kpts, kpts,threshold=MATCHING_THRESH)
                c3 = image.match_descriptor(leo_kpts, kpts,threshold=MATCHING_THRESH)
                c4 = image.match_descriptor(taiga_kpts, kpts,threshold=MATCHING_THRESH)
                # If more than 10% of the keypoints match draw the matching set
                # find the maximum in C1-4[6]
                c[0]= 0
                c[1]=c1[6]
                c[2]=c2[6]
                c[3]=c3[6]
                c[4]=c4[6]
                #print(c)
                c[0]=c[1] #init c[0]
                m=1
                for j in range(2):
                    if (c[0]<c[j+2] ):
                        m=j+2
                        c[0]=c[j+2]

                if (c[0]>0 ): # above a bar = matching someone
                    if (m==1):
                        FACE="ANDY"
                        print("Andy DETECTED","Match %d%%"%(100*c1[6]/KEYPOINTS_MAX))
                        i[1]=i[1]+1
                        x = c1[0]
                        y = c1[1]
                        x_error = x - (img.width()/2)
                        y_error = y - (img.height()/2)
                        x_pos += x_error * x_gain
                        y_pos += y_error * y_gain
                        # Clamp output between min and max
                        if (x_pos > x_max):
                            x_pos = x_max
                        if (x_pos < x_min):
                            x_pos = x_min
                        # Clamp output between min and max
                        if (y_pos > y_max):
                            y_pos = y_max
                        if (y_pos < y_min):
                            y_pos = y_min
                        red_led.on()
                        time.sleep(100)
                        red_led.off()
                    if (m==2):
                        FACE="AYA"
                        print("Aya DETECTED","Match %d%%"%(100*c2[6]/KEYPOINTS_MAX))
                        i[2]=i[2]+1
                        x = c2[0]
                        y = c2[1]
                        x_error = x - (img.width()/2)
                        y_error = y - (img.height()/2)
                        x_pos += x_error * x_gain
                        y_pos += y_error * y_gain
                        # Clamp output between min and max
                        if (x_pos > x_max):
                            x_pos = x_max
                        if (x_pos < x_min):
                            x_pos = x_min
                        # Clamp output between min and max
                        if (y_pos > y_max):
                            y_pos = y_max
                        if (y_pos < y_min):
                            y_pos = y_min
                        green_led.on()
                        red_led.on()
                        time.sleep(100)
                        green_led.off()
                        red_led.off()
                    if (m==3):
                        FACE="LEO"
                        print("Leo DETECTED","Match %d%%"%(100*c3[6]/KEYPOINTS_MAX))
                        i[3]=i[3]+1
                        x = c3[0]
                        y = c3[1]
                        x_error = x - (img.width()/2)
                        y_error = y - (img.height()/2)
                        x_pos += x_error * x_gain
                        y_pos += y_error * y_gain
                        # Clamp output between min and max
                        if (x_pos > x_max):
                            x_pos = x_max
                        if (x_pos < x_min):
                            x_pos = x_min
                        # Clamp output between min and max
                        if (y_pos > y_max):
                            y_pos = y_max
                        if (y_pos < y_min):
                            y_pos = y_min
                        blue_led.on()
                        time.sleep(100)
                        blue_led.off()
                    if (m==4):
                        FACE="TAIGA"
                        print("Taiga DETECTED","Match %d%%"%(100*c4[6]/KEYPOINTS_MAX))
                        i[4]=i[4]+1
                        x = c4[0]
                        y = c4[1]
                        x_error = x - (img.width()/2)
                        y_error = y - (img.height()/2)
                        x_pos += x_error * x_gain
                        y_pos += y_error * y_gain
                        # Clamp output between min and max
                        if (x_pos > x_max):
                            x_pos = x_max
                        if (x_pos < x_min):
                            x_pos = x_min
                        # Clamp output between min and max
                        if (y_pos > y_max):
                            y_pos = y_max
                        if (y_pos < y_min):
                            y_pos = y_min
                        green_led.on()
                        time.sleep(100)
                        green_led.off()

            # make decision based on times of matching for each person
            # find the maximum in i[1-4]
            i[0]=i[1] #init i[0] and m
            m=1
            for j in range(2):
                if (i[0]<i[j+2] ):
                    m=j+2
                    i[0]=i[j+2]
            if (i[m]>5): # conclued the decision and init the i[1-4]
                if (m==1):
                    print("Andy")
                    print("x-servo: %d y-servo: %d"%(int(x_pos),int(y_pos)))
                    #i2c.send('a',22)
                if (m==2):
                    print("Aya")
                    print("x-servo: %d y-servo: %d"%(int(x_pos),int(y_pos)))
                    #i2c.send('y',22)
                if (m==3):
                    print("Leo")
                    print("x-servo: %d y-servo: %d"%(int(x_pos),int(y_pos)))
                    #i2c.send('l',22)
                if (m==4):
                    print("Taiga")
                    print("x-servo: %d y-servo: %d"%(int(x_pos),int(y_pos)))
                    #i2c.send('t',22)
                for j in range(4):
                    i[j]=0


