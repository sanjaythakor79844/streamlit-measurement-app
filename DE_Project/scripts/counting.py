# import streamlit as st
# import requests
# import cv2
# import numpy as np
# import time

# ESP32_IP = "192.168.160.11"
# STREAM_URL = f"http://{ESP32_IP}/stream"
# STATUS_URL = f"http://{ESP32_IP}/status"
# RESET_URL = f"http://{ESP32_IP}/reset"

# def get_stream_frame():
#     try:
#         stream = requests.get(STREAM_URL, stream=True, timeout=5)
#         byte_data = b""
#         for chunk in stream.iter_content(chunk_size=1024):
#             byte_data += chunk
#             start = byte_data.find(b"\xff\xd8")
#             end = byte_data.find(b"\xff\xd9")
#             if start != -1 and end != -1:
#                 jpg = byte_data[start:end+2]
#                 byte_data = byte_data[end+2:]
#                 frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                 return frame
#     except:
#         return None

# def get_status():
#     try:
#         res = requests.get(STATUS_URL, timeout=2)
#         if res.status_code == 200:
#             return res.json()
#     except:
#         return None

# def reset_count():
#     try:
#         res = requests.get(RESET_URL, timeout=2)
#         if res.status_code == 200:
#             st.success("✅ Object count reset successfully!")
#         else:
#             st.warning("⚠️ Reset failed.")
#     except:
#         st.error("❌ ESP32 not reachable for reset.")

# def process_video(video_placeholder, stats_placeholder):
#     while st.session_state.get("video_running", False):
#         frame = get_stream_frame()
#         status = get_status()

#         count = 0
#         dist = 0

#         if status:
#             count = status.get("object_count", 0)
#             dist = status.get("last_distance_cm", 0)

#         stats_placeholder.markdown(f"### 📦 Count: {count} &nbsp;&nbsp;&nbsp;&nbsp; 📏 Distance: {dist:.2f} cm")

#         if frame is not None:
#             resized = cv2.resize(frame, (640, 480))
#             rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
#             video_placeholder.image(rgb, channels="RGB")
#         else:
#             video_placeholder.warning("⚠️ Frame not available from ESP32")

#         time.sleep(0.1)

import streamlit as st
import requests
import cv2
import numpy as np
import time

ESP32_IP = "192.168.160.11"
STREAM_URL = f"http://{ESP32_IP}/stream"
STATUS_URL = f"http://{ESP32_IP}/status"
RESET_URL = f"http://{ESP32_IP}/reset"

def get_stream_frame():
    try:
        stream = requests.get(STREAM_URL, stream=True, timeout=5)
        byte_data = b""
        for chunk in stream.iter_content(chunk_size=1024):
            byte_data += chunk
            start = byte_data.find(b"\xff\xd8")
            end = byte_data.find(b"\xff\xd9")
            if start != -1 and end != -1:
                jpg = byte_data[start:end + 2]
                byte_data = byte_data[end + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return frame
    except:
        return None

def get_status():
    try:
        res = requests.get(STATUS_URL, timeout=2)
        if res.status_code == 200:
            return res.json()
    except:
        return None

def reset_count():
    try:
        res = requests.get(RESET_URL, timeout=2)
        if res.status_code == 200:
            st.success("✅ Object count reset successfully!")
        else:
            st.warning("⚠️ Reset failed.")
    except:
        st.error("❌ ESP32 not reachable for reset.")

def process_video(video_placeholder, stats_placeholder):
    while st.session_state.get("video_running", False):
        frame = get_stream_frame()
        status = get_status()

        count = 0
        dist = 0

        if status:
            count = status.get("object_count", 0)
            dist = status.get("last_distance_cm", 0)

        # Update stats
        stats_placeholder.markdown(f"### 📦 Count: {count} &nbsp;&nbsp;&nbsp;&nbsp; 📏 Distance: {dist:.2f} cm")

        if frame is not None:
            resized = cv2.resize(frame, (640, 480))
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            video_placeholder.image(rgb, channels="RGB")
        else:
            video_placeholder.warning("⚠️ Frame not available from ESP32")

        # Slow down the loop to avoid overloading the system and control refresh rate
        time.sleep(0.1)

