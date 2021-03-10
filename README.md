## Tortoise Tracking

This program was created for use on a Raspberry Pi with the camera module. It utilizes OpenCV to detect motion in my tortoises cage. As the camera is at an angle, the image is warped so that it is proportional to the cage. Motion is detected and the pixel location is recorded. Pixel locations are averaged over the last 5 measurements and written to a csv file. The Raspberry Pi is turned on and off the the heat lamp timers so a cron job runs a bash script to start the tortoise tracking program.

# Image showing one days worth of recorded points

![alt text](https://github.com/oh-en/Tracking-Tortoise/blob/master/20200915.png?raw=true)