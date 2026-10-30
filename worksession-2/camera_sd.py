import os
import time
import board
import busio
import espcamera
import sdcardio
import storage

# --- SD card (slot on the XIAO ESP32S3 Sense expansion board) ---
# The SD card needs MISO too, unlike the display-only SPI in your original code
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# The Sense board's SD chip-select is GPIO21. If board.SDCS isn't defined in your
# build, use:  import microcontroller; cs = microcontroller.pin.GPIO21
sd = sdcardio.SDCard(spi, board.SDCS)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")

# --- Camera in JPEG mode ---
cam_i2c = busio.I2C(board.CAM_SCL, board.CAM_SDA)
cam = espcamera.Camera(
    data_pins=board.CAM_DATA,
    external_clock_pin=board.CAM_XCLK,
    pixel_clock_pin=board.CAM_PCLK,
    vsync_pin=board.CAM_VSYNC,
    href_pin=board.CAM_HREF,
    pixel_format=espcamera.PixelFormat.JPEG,
    frame_size=espcamera.FrameSize.SVGA,    # 800x600; try UXGA for 1600x1200
    i2c=cam_i2c,
    external_clock_frequency=20_000_000,
    framebuffer_count=1,
    jpeg_quality=12,                        # lower number = better quality, bigger file
    grab_mode=espcamera.GrabMode.LATEST)

# Let auto-exposure / white balance settle. The first frames are often dark or tinted.
for _ in range(5):
    cam.take(1)
    time.sleep(0.1)

def next_filename():
    existing = os.listdir("/sd")
    n = 0
    while f"img{n:04d}.jpg" in existing:
        n += 1
    return f"/sd/img{n:04d}.jpg"

frame = cam.take(1)
if frame is None:
    print("Capture failed")
else:
    path = next_filename()
    with open(path, "wb") as f:
        f.write(frame)
    print(f"Saved {path} ({len(frame)} bytes)")

storage.umount("/sd")
