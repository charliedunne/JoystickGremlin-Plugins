
import time
import math

import gremlin
from gremlin.user_script import *
from vjoy.vjoy import VJoyProxy


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

mode = ModeVariable(
    "Mode",
    "The mode in which to use this mapping",
    False
)

vjoy_axis = VirtualInputVariable(
    "Virtual output axis",
    "The vJoy axis to send the filtered output to.",
    False,
    [gremlin.common.InputType.JoystickAxis]
)

joy_axis = PhysicalInputVariable(
    "Physical input axis",
    "The physical input axis being filtered.",
    False,
    [gremlin.common.InputType.JoystickAxis]
)

deadzone = IntegerVariable(
    "Deadzone (%)",
    "Dynamic deadzone as percentage of total axis travel.",
    False,
    3,
    0,
    10
)

smoothing_time = IntegerVariable(
    "Smoothing time (ms)",
    "Higher values produce slower and more stable output.",
    False,
    500,
    50,
    2000
)


# --------------------------------------------------
# GLOBAL VARIABLES
# --------------------------------------------------

g_vjoy = VJoyProxy()

g_filtered_value = None
g_last_update = None


# --------------------------------------------------
# FILTER
# --------------------------------------------------

def filter_axis(input_value):

    global g_filtered_value
    global g_last_update

    now = time.time()

    # Initialize filter with first physical reading.
    if g_filtered_value is None:

        g_filtered_value = input_value
        g_last_update = now

        return g_filtered_value

    # Time elapsed since last update.
    dt = now - g_last_update
    g_last_update = now

    # Prevent excessively large time steps.
    dt = max(0.001, min(dt, 0.05))

    # Dynamic deadzone.
    # Joystick axis normally ranges from -1.0 to +1.0.
    threshold = (deadzone.value / 100.0) * 2.0

    # Difference between current input and filtered output.
    difference = input_value - g_filtered_value

    # Ignore small fluctuations.
    if abs(difference) <= threshold:
        return g_filtered_value

    # Exponential Moving Average.
    tau = smoothing_time.value / 1000.0

    alpha = 1.0 - math.exp(-dt / tau)

    # Smoothly approach the physical input.
    g_filtered_value += alpha * difference

    return g_filtered_value


# --------------------------------------------------
# VJOY OUTPUT
# --------------------------------------------------

def update_vjoy(value):

    g_vjoy[vjoy_axis.vjoy_id].axis(
        vjoy_axis.input_id
    ).value = value


# --------------------------------------------------
# PHYSICAL AXIS CALLBACK
# --------------------------------------------------

@joy_axis.decorator(mode)
def axis_cb(event):

    filtered = filter_axis(event.value)

    update_vjoy(filtered)
