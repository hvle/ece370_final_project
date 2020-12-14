#!/usr/bin/env python

import rospy
import os
import sys, select, termios, tty
from std_msgs.msg import String

msg = """
---------------------------
Moving around:
        w    
   a    s    d
---------------------------
q : Set velocity increments to 1.5
e : Set velocity increments to 0.5
r : Stop robot and reset all movement settings
anything else : stop

CTRL-C to quit
"""

print(msg)

def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


# def vels(speed, turn):
#     return "currently:\tspeed %s\tturn %s " % (speed,turn)

###############################################################################

settings = termios.tcgetattr(sys.stdin)
rospy.init_node('teleop_twist_keyboard')
pub = rospy.Publisher('/key_press', String, queue_size=1)

key_timeout = rospy.get_param("~key_timeout", 0.0)
if key_timeout == 0.0:
    key_timeout = None
try:
    while not rospy.is_shutdown():
        key = getKey(key_timeout)
        # joint_left = "dd_robot::left_wheel_hinge"
        # joint_right = "dd_robot::right_wheel_hinge"
        # msg_topic_feedback = "/gazebo/get_joint_properties"
        # pub_feedback = rospy.ServiceProxy(msg_topic_feedback, GetJointProperties)

        # left_feedback = pub_feedback(joint_left)
        # right_feedback = pub_feedback(joint_right)
        # print("Left Wheel Rate:", left_feedback.rate)
        # print("Right Wheel Rate:", right_feedback.rate)
        print(key)

        pub.publish(key)
        if (key == '\x03'):
            break
        

except Exception as e:
    print(e)

finally:
    print("")
    print("------------------------------------------")
    print("Exiting Keyboard Controller...")
    print("Attempting to kill hvle_move_robot node...")
    os.system("rosnode kill hvle_move_robot")
    print("------------------------------------------")
    print("")
    print("Complete...")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)