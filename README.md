# Tortoise Tracking

This program was created for use on a Raspberry Pi with the camera module. It utilizes OpenCV to detect motion in my tortoises cage. As the camera is at an angle, the image is warped so that it is proportional to the cage. Motion is detected and the pixel location is recorded. Pixel locations are averaged over the last 5 measurements and written to a csv file. The Raspberry Pi is turned on and off with the heat lamp timers so a cron job runs a bash script to start the tortoise tracking program.

## Image showing one days worth of recorded points

![alt text](https://github.com/oh-en/Tracking-Tortoise/blob/master/20200916.png?raw=true)

#### Areas of Improvement

This program would be improved with a more accurate location reading. First, motion was not always detected in the dark section of the enclosure. Second, I initially tried using object detection but the tortoises shell pattern could not always be picked up by the algorithm. Once the image was lost, it could not be recovered. To improve, a better object detection method will need to be used. I attempted using the object detection classes built in the OpenCV but those were not successful for me. To get this program working efficiently, I decided to use motion detection instead which compares the pixel difference between two photos. This worked well for the most part. Sometimes the tortoise would dig with his front hand and then his back hand afterwards. This would be picked up and recorded as movement despite the tortoises main shell being stationary. I could have included a threshold for the magnitude of movement detected. I decided to average the movement over the previous 5 locations.

#### Information Gathered

This tortoise walks a lot! Preliminary measurements indicate that on his most traveled day, he walked about a mile. These measurements are of course not the most accurate. This distance was taken by computing the sum of distances between each pixel measurement. There are major variations in each measurement. Generally, the only thing moving in the cage should be the tortoise but movement was picked up by the program in the reflection on the heat lamp. You can also see the no movement was detected in the darker areas of the image despite the tortoise walking in those areas.

It can also be seen that the tortoise spends significantly more time at his food bowl than he does his large water dish. Geno walks numerous laps around the edge of the cage with occasional trips over his log.