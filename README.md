# Water room system
A water room system used to solve the problem of the serious congestion in campus water room during the peak hours of water use.



## Start-up

Deploy the code separately to the micro-controller, server, and WeChat mini program. Then modify the network and MySQL database configuration in the code.

To get the server to work, run all the codes under the folder `run`.

Remember to enable MySQL service and create database and table, the code for table creating is as follows.

```mysql
CREATE TABLE information_system (
    water_room_id INT(32) UNSIGNED PRIMARY KEY,
    status BOOLEAN NOT NULL DEFAULT 0,
    queuing_number INT(32) UNSIGNED NOT NULL
);
INSERT INTO information_system (water_room_id, status, queuing_number) VALUES (1, 1, 3);
INSERT INTO information_system (water_room_id, status, queuing_number) VALUES (2, 0, 0);
INSERT INTO information_system (water_room_id, status, queuing_number) VALUES (3, 1, 2);
```



## Structure

### ESP32-CAM

Use ESP32-CAM for data collection and transmission to the server, including light information and queuing image of the water room.



### Server

Receive information and perform image processing, save data to the database and provide interface for the upper layer.

#### run

Including files used to start the server.

+ `run_mysql_server.py` : Used to open the connection with the micro-controller.
+ `run_tcp_server.py` : Used to open interfaces for the front-end.

#### yolov5_train

Including the trained YOLOv5 model with training dataset and results.

The final weight file used for prediction is `yolov5-master/water_room_system.pt`

#### tmp

Save temporary files, specifically the image data and visualized results after image processing.

#### test_script

*Useless at the moment.* 

Used to test the code during the developing process.



### WeChat

The front end.



## Tips

If you don’t want to use the light sensor in practical, you can remove the annotation `// #define LIGHT_SIMULATE` to enable light simulation. It will simulate the input of the light sensor at the software level.
