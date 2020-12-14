#!/bin/sh

# Deleting All Models
rosservice call gazebo/delete_model final_setup_test
rosservice call gazebo/delete_model dd_robot
rosservice call gazebo/delete_model final_setup

