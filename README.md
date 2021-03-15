# Tortoise Tracking

This program was created for use on a Raspberry Pi with the camera module. It utilizes OpenCV to detect motion in my tortoise's cage. As the camera is at an angle, the image is warped so that it is proportional to the cage. This is so that it will be easier to translate between a pixel distance and a distance in centimeters. Motion is detected and the pixel location is recorded. Pixel locations are averaged over the last 5 measurements and written to a csv file. This is done in an attempt to smooth out any erroneous detections. The Raspberry Pi is turned on and off with the heat lamp timers so a cron job runs a bash script at boot to start the tortoise tracking program.

## Image showing one days worth of recorded points

![alt text](https://github.com/oh-en/Tracking-Tortoise/blob/master/20200920.png?raw=true)

It can also be seen that the tortoise spends significantly more time at his food bowl than he does his large water dish. The tortoise walks numerous laps around the edge of the cage with occasional trips over his log.

#### Information Gathered

This tortoise walks a lot! Preliminary measurements indicate that on his most traveled day, he walked about 1.2 miles. These measurements are of course not the most accurate. This distance was taken by computing the sum of distances between each pixel measurement. There are major variations in each measurement. Generally, the only thing moving in the cage should be the tortoise but movement was picked up by the program in the reflection on the heat lamp. You can also see that no movement was detected in the darker areas of the image despite the tortoise walking in those areas.

![alt text](https://github.com/oh-en/Tracking-Tortoise/blob/master/cumulative_distance.png?raw=true)

As can be seen in the cumulative distance graph, the tortoise is consistently active from 8am until about 5 or 6pm when activity subsides. This is likely due to the summer months being much hotter. From personal experience, the tortoise walks less during the winter so further testing during winter months will need to be done to confirm this hypothesis.

![alt text](https://github.com/oh-en/Tracking-Tortoise/blob/master/velocity_histogram.png?raw=true)

The histogram of velocity measurements shows that the tortoise generally walks at a speed between 2.5 and 5 cm/s. The median magnitude of velocity is 6.4 cm/s but this measurement includes many erroneous higher values. These higher values come from when motion is detected in incorrect locations. When limiting the max velocity that can be measured to 20 cm/s, the median velocity is 3.7 cm/s.

#### Areas of Improvement

This program would be improved with a more accurate location reading. First, motion was not always detected in the dark section of the enclosure. Second, I initially tried using object detection but the tortoises shell pattern could not always be picked up by the algorithm. Once the image was lost, it could not be recovered. To improve, a better object detection method will need to be used. I attempted using the object detection classes built in the OpenCV but those were not successful for me. To get this program working efficiently, I decided to use motion detection instead which compares the pixel difference between two photos. This worked well for the most part. Sometimes the tortoise would dig with his front hand and then his back hand afterwards. This would be picked up and recorded as movement despite the tortoises main shell being stationary. I could have included a threshold for the magnitude of movement detected. I decided to average the movement over the previous 5 locations to smooth out the measurements and lessen the impact of incorrect readings. In addition, I used a fan to cool the Raspberry Pi and unfortunately, due to the tortoise activity, a lot of dust was kicked up and resulted in overheating. The Raspberry Pi would refuse to boot after about 10 days of running this program due to an accumulation of dirt on the system.

## Gif showing most recent 20 points connected

![alt text](https://github.com/oh-en/Tracking-Tortoise/blob/master/tortoise.gif?raw=true)
