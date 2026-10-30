
import os
import time
import board
import busio
import espcamera
 
SAVE_DIR = "/images"
 
# --- Check that the flash is writable before doing anything else ---
def flash_is_writable():
    try:
        with open("/.write_test", "w") as f:
            f.write("ok")
        os.remove("/.write_test")
        return True
    except OSError as e:
        if e.errno == 30:  # EROFS: read-only filesystem
            return False
        raise
 
if not flash_is_writable():
    print("Flash is read-only.")
    print("Jumper D0 to GND and press reset to let code write to CIRCUITPY.")
    while True:
        time.sleep(1)
 
# Make the images folder if it doesn't exist yet
try:
    os.mkdir(SAVE_DIR)
except OSError:
    pass  # already exists
 
# --- Camera in JPEG mode ---
cam_i2c = busio.I2C(board.CAM_SCL, board.CAM_SDA)
cam = espcamera.Camera(
    data_pins=board.CAM_DATA,
    external_clock_pin=board.CAM_XCLK,
    pixel_clock_pin=board.CAM_PCLK,
    vsync_pin=board.CAM_VSYNC,
    href_pin=board.CAM_HREF,
    pixel_format=espcamera.PixelFormat.JPEG,
    frame_size=espcamera.FrameSize.SVGA,    # 800x600; UXGA = 1600x1200
    i2c=cam_i2c,
    external_clock_frequency=20_000_000,
    framebuffer_count=1,
    jpeg_quality=12,                        # lower = better quality, bigger file
    grab_mode=espcamera.GrabMode.LATEST)
 
# Let auto-exposure and white balance settle
for _ in range(5):
    cam.take(1)
    time.sleep(0.1)
 
def next_filename():
    existing = os.listdir(SAVE_DIR)
    n = 0
    while f"img{n:04d}.jpg" in existing:
        n += 1
    return f"{SAVE_DIR}/img{n:04d}.jpg"
 
def free_space():
    s = os.statvfs("/")
    return s[0] * s[3]  # block size * free blocks
 
# --- Take and save the photo ---
frame = cam.take(1)
if frame is None:
    print("Capture failed")
elif len(frame) > free_space():
    print(f"Not enough space: photo is {len(frame)} bytes, "
          f"only {free_space()} free")
else:
    path = next_filename()
    try:
        with open(path, "wb") as f:
            f.write(frame)
        print(f"Saved {path} ({len(frame)} bytes, {free_space()} bytes free)")
    except OSError as e:
        print("Write failed:", e)
 
cam.deinit()
print("Done. Remove the D0 jumper and reset to view photos on your computer.")
