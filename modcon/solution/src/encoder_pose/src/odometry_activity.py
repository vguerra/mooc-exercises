#!/usr/bin/env python
# coding: utf-8

# In[1]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your DeltaPhi function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

#TODO: write a correct function

def DeltaPhi(encoder_msg, prev_ticks):
    """
        Args:
            encoder_msg: ROS encoder message (ENUM)
            prev_ticks: Previous tick count from the encoders (int)
        Return:
            rotation_wheel: Rotation of the wheel in radians (double)
            ticks: current number of ticks (int)
    """
    
    # TODO: these are random values, you have to implement your own solution in here
    delta_ticks = encoder_msg.data - prev_ticks     
    delta_phi = delta_ticks * 2 * np.pi / encoder_msg.resolution

    return delta_phi, encoder_msg.data

# In[2]:


# The function written in this cell will actually be ran on your robot (sim or real). 
# Put together the steps above and write your odometry function! 
# DO NOT CHANGE THE NAME OF THIS FUNCTION, INPUTS OR OUTPUTS, OR THINGS WILL BREAK

# TODO: write the odometry function

import numpy as np 

def poseEstimation( R, # radius of wheel (assumed identical) - this is fixed in simulation, and will be imported from your saved calibration for the physical robot
                    baseline_wheel2wheel, # distance from wheel to wheel; 2L of the theory
                    x_prev, # previous x estimate - assume given
                    y_prev, # previous y estimate - assume given
                    theta_prev, # previous orientation estimate - assume given
                    delta_phi_left, # left wheel rotation (rad)
                    delta_phi_right): # right wheel rotation (rad)
    
    """
        Calculate the current Duckiebot pose using the dead-reckoning approach.

        Returns x,y,theta current estimates:
            x_curr, y_curr, theta_curr (:double: values)
    """
    
    # TODO: these are random values, you have to implement your own solution in here
    d_left = R * delta_phi_left
    d_right = R * delta_phi_right
    d_travelled = (d_right + d_left)*0.5
    delta_theta = (d_right - d_left)/baseline_wheel2wheel
    delta_x = d_travelled * np.cos(theta_prev)
    delta_y = d_travelled * np.sin(theta_prev)
    x_curr = x_prev + delta_x
    y_curr = y_prev + delta_y 
    theta_curr = theta_prev + delta_theta 

    return x_curr, y_curr, theta_curr
