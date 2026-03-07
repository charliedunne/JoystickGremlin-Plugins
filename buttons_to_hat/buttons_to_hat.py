import gremlin
from gremlin.user_script import *


mode = ModeVariable(
    "Mode",
    "The mode to use for this mapping",
    False
)
vjoy_hat = VirtualInputVariable(
    "Output Hat",
    "vJoy hat to use as the output",
    False,
    [gremlin.common.InputType.JoystickHat]
)
btn_1 = PhysicalInputVariable(
    "Button Up",
    "Button which will be mapped to the up direction of the hat.",
    False,
    [gremlin.common.InputType.JoystickButton]
)
btn_2 = PhysicalInputVariable(
    "Button Right",
    "Button which will be mapped to the right direction of the hat.",
    False,
    [gremlin.common.InputType.JoystickButton]
)
btn_3 = PhysicalInputVariable(
    "Button Down",
    "Button which will be mapped to the down direction of the hat.",
    False,
    [gremlin.common.InputType.JoystickButton]
)
btn_4 = PhysicalInputVariable(
    "Button Left",
    "Button which will be mapped to the left direction of the hat.",
    False,
    [gremlin.common.InputType.JoystickButton]
)

state = [0, 0]


def set_state(vjoy):
    device = vjoy[vjoy_hat.vjoy_id]
    device.hat(vjoy_hat.vjoy_id).direction  = \
        gremlin.types.HatDirection.to_enum(tuple(state))


@btn_1.decorator(mode)
def button_1(event, vjoy):
    global state
    state[1] = 1 if event.is_pressed else 0
    set_state(vjoy)


@btn_2.decorator(mode)
def button_2(event, vjoy):
    global state
    state[0] = 1 if event.is_pressed else 0
    set_state(vjoy)


@btn_3.decorator(mode)
def button_3(event, vjoy):
    global state
    state[1] = -1 if event.is_pressed else 0
    set_state(vjoy)


@btn_4.decorator(mode)
def button_4(event, vjoy):
    global state
    state[0] = -1 if event.is_pressed else 0
    set_state(vjoy)
