# boot.py
import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D0)
switch.switch_to_input(pull=digitalio.Pull.UP)

# D0 jumpered to GND at startup -> code can write, computer can't
# D0 left floating             -> normal mode, you can edit files from your computer
if not switch.value:
    storage.remount("/", readonly=False)
