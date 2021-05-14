#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

# Lateral control

# TODO: write the PID controller using what you've learned in the previous activities

# Note: y_hat will be calculated based on your DeltaPhi() and poseEstimate() functions written previously 

def PIDController(
    v_0, # assume given (by the scenario)
    y_ref, # assume given (by the scenario)
    y_hat, # assume given (by the odometry)
    prev_e_y, # assume given (by the previous iteration of this function)
    prev_int_y, # assume given (by the previous iteration of this function)
    delta_t): # assume given (by the simulator)
    """
    Args:
        v_0 (:double:) linear Duckiebot speed.
        y_ref (:double:) reference lateral pose
        y_hat (:double:) the current estiamted pose along y.
        prev_e_y (:double:) tracking error at previous iteration.
        prev_int_y (:double:) previous integral error term.
        delta_t (:double:) time interval since last call.
    returns:
        v_0 (:double:) linear velocity of the Duckiebot 
        omega (:double:) angular velocity of the Duckiebot
        e_y (:double:) current tracking error (automatically becomes prev_e_y at next iteration).
        e_int_y (:double:) current integral error (automatically becomes prev_int_y at next iteration).
    """
    # (21_05_11_11_32_45 = 000 - 41.21 ; 001 - 14.35)
    # Kp = 1.75, Kd = 0.0, Ki = 0.0

    # (21_05_12_11_41_47 = 000 - 60.00 ; 001 - 20.00)
    # Kp = 1.75, Kd = 10.0, Ki = 0.0

    # (21_05_12_12_37_49 = 000 - 60.00 ; 001 - 28.15)
    # Kp = 1.75, Kd = 50.0, Ki = 0.0

    # (21_05_14_10_53_25 = 000 - 60.00 ; 001 - 28.35)
    # Kp = 3.00, Kd = 60.57, Ki = 0.17

    # Tu = 17, Kp = 0.75, Ti = 8.5, Td = 2.1
    # Tu = 12, Kp = 1.75
    
    Kp = 6.00
    Kd = 60.57
    Ki = 0.17
    boundary_int_y = 0.5
    max_omega = 8.0
    e_y = y_ref - y_hat
    e_der_y = (e_y - prev_e_y)/delta_t
    e_int_y = prev_int_y + e_y * delta_t
    e_int_y = max(min(e_int_y, boundary_int_y), -boundary_int_y)
    omega = Kp*e_y + Ki*e_int_y + Kd*e_der_y
#     print(e_y, omega)
#     omega = max(min(omega, boundary_omega), -boundary_omega)

    if False:
        print(f"v_0 = {v_0}")
        print(f"y_ref = {y_ref}")
        print(f"prev_e_y = {prev_e_y}")
        print(f"prev_int_y = {prev_int_y}")
        print(f"y_hat = {y_hat}")
        print(f"delta_t = {delta_t}")
        print(f"e_y = {e_y}")
        print(f"e_der_y = {e_der_y}")
        print(f"e_int_y = {e_int_y}")
        print(f"omega = {omega}")
        if omega > 0:
            print("turning LEFT")
        else:
            print("turning RIGHT")

    return [v_0, omega], e_y, e_int_y

