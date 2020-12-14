#!/bin/sh

rosservice call gazebo/delete_model dd_robot
rosrun gazebo_ros spawn_model -file ~/catkin_ws/src/hle25_final/models/model.sdf -sdf -x 0 -y 0 -z .1 -model dd_robot
