import time
self.run_action("{PHOTO_LIGHT_ON_ONLY_ON_ID}")  # Photo Light On Only (ON)
time.sleep(3)
self.run_action("{DSLR_FOCUS_ON_ID}")  # Stage 1 On
time.sleep(1)
self.run_action("{DSLR_SHUTTER_ON_ID}")  # Stage 2 On
time.sleep(1)
self.run_action("{DSLR_SHUTTER_OFF_ID}")  # Stage 2 Off
time.sleep(1)
self.run_action("{DSLR_FOCUS_OFF_ID}")  # Stage 1 Off
self.run_action("{PHOTO_LIGHT_ON_ONLY_OFF_ID}")  # Photo Light On Only (OFF)