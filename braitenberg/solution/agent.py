#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Optional, Tuple

import math
import numpy as np
from aido_schemas import (
    Context,
    DB20Commands,
    DB20Observations,
    EpisodeStart,
    GetCommands,
    JPGImage,
    LEDSCommands,
    protocol_agent_DB20,
    PWMCommands,
    RGB,
    wrap_direct,
)

import duckietown_code_utils as dcu
from connections import get_motor_left_matrix, get_motor_right_matrix
from preprocessing import preprocess


@dataclass
class BraitenbergAgentConfig:
    gain: float = 0.4
    const: float = 0.6


class BraitenbergAgent:
    config = BraitenbergAgentConfig()

    left: Optional[np.ndarray]
    right: Optional[np.ndarray]
    rgb: Optional[np.ndarray]
    l_max: float
    r_max: float
    l_min: float
    r_min: float

    def init(self, context: Context):
        context.info("init()")
        self.rgb = None
        self.l_fwd_max = -math.inf
        self.r_fwd_max = -math.inf
        self.l_fwd_min = math.inf
        self.r_fwd_min = math.inf
        self.l_bwd_max = -math.inf
        self.r_bwd_max = -math.inf
        self.l_bwd_min = math.inf
        self.r_bwd_min = math.inf
        self.left = None
        self.right = None

    def on_received_seed(self, data: int):
        np.random.seed(data)

    def on_received_episode_start(self, context: Context, data: EpisodeStart):
        context.info(f'Starting episode "{data.episode_name}".')

    def on_received_observations(self, context: Context, data: DB20Observations):
        camera: JPGImage = data.camera
        if self.rgb is None:
            context.info("received first observations")
        self.rgb = dcu.bgr_from_rgb(dcu.bgr_from_jpg(camera.jpg_data))

    def compute_commands(self, context:Context) -> Tuple[float, float]:
        """ Returns the commands (pwm_left, pwm_right) """
        # If we have not received any image, we don't move
        if self.rgb is None:
            return 0.0, 0.0

        if self.left is None:
            # if it is the first time, we initialize the structures
            shape = self.rgb.shape[0], self.rgb.shape[1]
            self.left = get_motor_left_matrix(shape)
            self.right = get_motor_right_matrix(shape)

        # let's take only the intensity of RGB
        P = preprocess(self.rgb)
        # now we just compute the activation of our sensors
        l = float(np.sum(P * self.left))
        r = float(np.sum(P * self.right))
        # context.info(f"left raw: {l}, right raw: {r}")

        gain = self.config.gain
        const = self.config.const
        bwd_gain = 0.1

        if l < 0.0:
            self.l_bwd_max = max(-l, self.l_bwd_max)
            self.l_bwd_min = min(-l, self.l_bwd_min)
            ls = rescale(-l, self.l_bwd_min, self.l_bwd_max)
            pwm_left = -ls * bwd_gain
            # context.info(f"pwm left: {pwm_left}, pwm right: {-pwm_left}")
            return (pwm_left, -pwm_left)
        else:
            self.l_fwd_max = max(l, self.l_fwd_max)
            self.l_fwd_min = min(l, self.l_fwd_min)
            ls = rescale(l, self.l_fwd_min, self.l_fwd_max)
            pwm_left = const + ls * gain

        if r < 0.0:
            self.r_bwd_max = max(-r, self.r_bwd_max)
            self.r_bwd_min = min(-r, self.r_bwd_min)
            rs = rescale(-r, self.r_bwd_min, self.r_bwd_max)
            pwm_right = -rs * bwd_gain
            # context.info(f"pwm left: {-pwm_right}, pwm right: {pwm_right}")
            return (-pwm_right, pwm_right)
        else:
            self.r_fwd_max = max(r, self.r_fwd_max)
            self.r_fwd_min = min(r, self.r_fwd_min)
            rs = rescale(r, self.r_fwd_min, self.r_fwd_max)
            pwm_right = const + rs * gain

        # context.info(f"pwm left: {pwm_left}, pwm right: {pwm_right}")
        return pwm_left, pwm_right

    def on_received_get_commands(self, context: Context, data: GetCommands):
        pwm_left, pwm_right = self.compute_commands(context)

        col = RGB(0.0, 0.0, 1.0)
        col_left = RGB(pwm_left, pwm_left, 0.0)
        col_right = RGB(pwm_right, pwm_right, 0.0)
        led_commands = LEDSCommands(col, col_left, col_right, col_left, col_right)
        pwm_commands = PWMCommands(motor_left=pwm_left, motor_right=pwm_right)
        commands = DB20Commands(pwm_commands, led_commands)
        context.write("commands", commands)

    def finish(self, context: Context):
        context.info("finish()")


def rescale(a: float, L: float, U: float):
    if np.allclose(L, U):
        return 0.0
    return (a - L) / (U - L)


def main():
    node = BraitenbergAgent()
    protocol = protocol_agent_DB20
    wrap_direct(node=node, protocol=protocol)


if __name__ == "__main__":
    main()
