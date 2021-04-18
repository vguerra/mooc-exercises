from typing import Tuple

import numpy as np


def get_motor_left_matrix_random(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")  # write your function instead of this one
    res[100:150, 100:150] = 1
    res[300:, 200:] = 1
    return res

def get_motor_right_matrix_random(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")  # write your function instead of this one
    res[100:150, 100:300] = -1
    return res


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")  # write your function instead of this one
    quarter_height = shape[0] // 4
    quarter_width = shape[1] // 4
    # res[:2*quarter_height, :quarter_width] = 1
    res[2*quarter_height:3*quarter_height, :quarter_width] = 2
    res[3*quarter_height:, :quarter_width] = 4
    # res[:2*quarter_height, quarter_width:2*quarter_width] = 2
    res[2*quarter_height:3*quarter_height, quarter_width:2*quarter_width] = 4
    res[3*quarter_height:, quarter_width:2*quarter_width] = 8
    
    # breaking
    # res[2*quarter_height:, 2*quarter_width:3*quarter_width] = -10
    # res[2*quarter_height:, 3*quarter_width:] = -8
    
    #res[:, quarter_width:2*quarter_width] = 1

    return res

def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")  # write your function instead of this one
    quarter_height = shape[0] // 4
    quarter_width = shape[1] // 4

    # res[:2*quarter_height, 2*quarter_width:3*quarter_width] = 2
    res[2*quarter_height:3*quarter_height, 2*quarter_width:3*quarter_width] = 4
    res[3*quarter_height:, 2*quarter_width:3*quarter_width] = 8
    # res[:2*quarter_height, 3*quarter_width:] = 1
    res[2*quarter_height:3*quarter_height, 3*quarter_width:] = 2
    res[3*quarter_height:, 3*quarter_width:] = 4
    
    #res[:, 2*quarter_width:3*quarter_width] = 1

    # breaking
    # res[2*quarter_height:3*quarter_height, quarter_width:2*quarter_width] = -10
    # res[2*quarter_height:3*quarter_height, :quarter_width] = -8

    return res

### Scenarios

# Left and Right full of 0s?
# R:/ It goes in a straight line

# Left full of ones?
# R:/ The car advances moving to the right all time

# Left and right full of ones?
# R:/ It goes in a straight line. So if
#     both matrices are equal, the robot goes straight.

# What would be a good strategy?
# R:/ 
# a. To put hight values on places where the duckie
#    will be detected close to the motor.
# b. Taking intou account proximity to center and to the lower
#    part of the image, as that means that duck is very close
#    and motor needs to increase speed.

# Submissions

# https://challenges.duckietown.org/v4/humans/submissions/14413
# dts challenges follow --submission 14413
