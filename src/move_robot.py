#! /usr/bin/env python

import rospy
from std_msgs.msg import String
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import GetJointProperties
import time

## move_robot_package
# Global Variables

# Desired Wheel Velocities
fl_vel_des = 0.0        # Front Left
fr_vel_des = 0.0        # Front Right
rl_vel_des = 0.0        # Rear Left
rr_vel_des = 0.0        # Rear Right

# Wheel Parameters
fw = 0.24   # Radius (m)
rw = 0.24   # Radius (m)

# Enable/Disable Feedback Controller
effort_controller = 1
speed_multiplier = 1.5



class Server:
    def __init__(self,*args, **kwargs):
        pass
    
    def keyboard_callback(self,msg):
        global fl_vel_des, fr_vel_des, rl_vel_des, rr_vel_des, effort_controller, speed_multiplier
        key = msg.data

        joint_front_left = "dd_robot::left_wheel_hinge"
        joint_front_right = "dd_robot::right_wheel_hinge"
        joint_rear_left = "dd_robot::rear_left_wheel_hinge"
        joint_rear_right = "dd_robot::rear_right_wheel_hinge"
        pub = rospy.ServiceProxy('/gazebo/apply_joint_effort', ApplyJointEffort)
        start_time = rospy.Time(0,0)
        end_time = rospy.Time(1.0,0)


        if key == "w":
            effort_controller = 1
            fl_vel_des += 1.0 * speed_multiplier
            fr_vel_des += 1.0 * speed_multiplier
            rl_vel_des += 1.0 * speed_multiplier
            rr_vel_des += 1.0 * speed_multiplier
        elif key == "s":
            effort_controller = 1
            fl_vel_des += -1.0 * speed_multiplier
            fr_vel_des += -1.0 * speed_multiplier
            rl_vel_des += -1.0 * speed_multiplier
            rr_vel_des += -1.0 * speed_multiplier
        elif key == "a":
            effort_controller = 0
            pub(joint_front_left,-2.0,start_time,end_time)
            pub(joint_front_right,2.0,start_time,end_time)
            effort_controller = 1
        elif key == "d":
            effort_controller = 0
            pub(joint_front_left,2.0,start_time,end_time)
            pub(joint_front_right,-2.0,start_time,end_time)
            effort_controller = 1
        elif key == "q":
            speed_multiplier = 1.5
        elif key == "e":
            speed_multiplier = 0.1
        elif key == "r":
            speed_multiplier = 1.5
            effort_controller = 1
            fl_vel_des = 0
            fr_vel_des = 0
            rl_vel_des = 0
            rr_vel_des = 0
        else:
            effort_controller = 1.0
            fl_vel_des = 0
            fr_vel_des = 0
            rl_vel_des = 0
            rr_vel_des = 0
            
    
       


    
# # print("Starting...")
rospy.init_node('hvle_move_robot')

joint_front_left = "dd_robot::left_wheel_hinge"
joint_front_right = "dd_robot::right_wheel_hinge"
joint_rear_left = "dd_robot::rear_left_wheel_hinge"
joint_rear_right = "dd_robot::rear_right_wheel_hinge"

msg_topic_feedback = "/gazebo/get_joint_properties"


server = Server()
rospy.Subscriber('/key_press', String, server.keyboard_callback)


pub = rospy.ServiceProxy('/gazebo/apply_joint_effort', ApplyJointEffort)
pub_feedback = rospy.ServiceProxy(msg_topic_feedback, GetJointProperties)
start_time = rospy.Time(0,0)
f = 0.5
T = 1/f
end_time = rospy.Time(T,0)
rate = rospy.Rate(f)

timeout = 0
while not rospy.is_shutdown():     
    try:
        # Front Left Rate
        val = pub_feedback(joint_front_left)
        fl_vel = val.rate[0]*fw
        # Front Right Rate
        val = pub_feedback(joint_front_right)
        fr_vel = val.rate[0]*fw
        # Rear Left Rate
        val = pub_feedback(joint_rear_left)
        rl_vel = val.rate[0]*rw
        # Rear Right Rate
        val = pub_feedback(joint_rear_right)
        rr_vel = val.rate[0]*rw

        if effort_controller:
            # Wheel Error (Desired Velocity - Actual Velocity)         
            fl_error = fl_vel_des - fl_vel
            fr_error = fr_vel_des - fr_vel
            rl_error = rl_vel_des - rl_vel
            rr_error = rr_vel_des - rr_vel

            kp = 1.5
            fl_effort = kp*fl_error
            fr_effort = kp*fr_error
            rl_effort = kp*rl_error
            rr_effort = kp*rr_error
            # Effort Limiter 
            if abs(fl_effort) > 2.0:
                if fl_effort > 0:
                    fl_effort = 2.0
                else:
                    fl_effort = -2.0                
            if abs(fr_effort) > 2.0:
                if fr_effort > 0:
                    fr_effort = 2.0
                else:
                    fr_effort = -2.0
            if abs(rl_effort) > 2.0:
                if rl_effort > 0:
                    rl_effort = 2.0
                else:
                    rl_effort = -2.0
            if abs(rr_effort) > 2.0:
                if rr_effort > 0:
                    rr_effort = 2.0
                else:
                    rr_effort = -2.0
            # print "    Feedback Controller: \tEnabled"
            pass
        else:
            # print "    Feedback Controller: \tDisabled"    
            pass
        if speed_multiplier == 0.1:
            # print "    Slow Speed: \t\tEnabled"
            pass
        else:
            # print "    Slow Speed: \t\tDisabled"
            pass
        # print "------------------------------------------------------------------------------------------"
        # print "\tJoint Name \t Desired Velocity (m/s)  Actual Velocity (m/s)  Applied Effort"
        # print "------------------------------------------------------------------------------------------"
        # print "    Front Left Wheel\t       " + "{:.3f}".format(fl_vel_des) + "\t\t      " + "{:.3f}".format(fl_vel) + "\t\t      " +  "{:.3f}".format(fl_effort)
        # print "    Front Right Wheel\t       " + "{:.3f}".format(fr_vel_des) + "\t\t      " + "{:.3f}".format(fr_vel) + "\t\t      " +  "{:.3f}".format(fr_effort)
        # print "    Rear Left Wheel\t       " + "{:.3f}".format(rl_vel_des) + "\t\t      " + "{:.3f}".format(rl_vel) + "\t\t      " +  "{:.3f}".format(rl_effort)
        # print "    Rear Left Wheel\t       " + "{:.3f}".format(rr_vel_des) + "\t\t      " + "{:.3f}".format(rr_vel) + "\t\t      " +  "{:.3f}".format(rr_effort)
        # print "------------------------------------------------------------------------------------------\n"

        pub(joint_front_left, fl_effort, start_time, end_time)
        pub(joint_front_right, fr_effort, start_time, end_time)
        pub(joint_rear_left, rl_effort, start_time, end_time) 
        pub(joint_rear_right, rr_effort, start_time, end_time)
        rate.sleep()
        timeout = 0
    except Exception as e:
        # print(e)
        fl_vel_des = 0
        fr_vel_des = 0
        rl_vel_des = 0
        rr_vel_des = 0
        effort_controller = 1
        speed_multiplier = 1.5
        if timeout == 10:
            # print "\n"
            # print "---------------------------------"
            # print "\tProgram Timed Out"
            # print "---------------------------------"
            break
        else:
            timeout += 1
            time.sleep(1)

            

        
    # rospy.spin()
    

    