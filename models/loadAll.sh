#!/bin/sh

# Deleting All Models
rosservice call gazebo/delete_model final_setup_test
rosservice call gazebo/delete_model dd_robot
rosservice call gazebo/delete_model final_setup

# Spawning All Models
rosrun gazebo_ros spawn_model -file final.sdf -sdf -model final_setup -y -0.0 -x -0.0 -z 0.0
rosrun gazebo_ros spawn_model -file final_test.sdf -sdf -model final_setup_test -y -0.0 -x -0.0 -z 0.0
sleep 2
rosrun gazebo_ros spawn_model -file ~/catkin_ws/src/hle25_final/models/model.sdf -sdf -x 0 -y 0 -z .1 -model dd_robot
