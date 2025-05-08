# import cv2
# import math
# import numpy as np
# import requests

# ESP32_URL = "http://192.168.25.11:81/stream"  # Replace with actual ESP32-CAM IP
# RATIO = 16 / 184.8  # Real-world measurement per pixel

# def get_esp32_frame():
#     """ Fetch a frame from ESP32-CAM MJPEG stream """
#     try:
#         stream = requests.get(ESP32_URL, stream=True, timeout=2)
#         byte_data = b""
        
#         for chunk in stream.iter_content(chunk_size=4096):
#             byte_data += chunk
#             a = byte_data.find(b'\xff\xd8')  # Start of JPEG
#             b = byte_data.find(b'\xff\xd9')  # End of JPEG
            
#             if a != -1 and b != -1:
#                 jpg = byte_data[a:b+2]
#                 byte_data = byte_data[b+2:]
#                 frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                 return frame
#     except requests.exceptions.RequestException as e:
#         print("⚠️ Error: Could not connect to ESP32-CAM", e)
#         return None

# # Main Loop
# while True:
#     frame = get_esp32_frame()
#     if frame is None:
#         continue  # Skip if no frame received

#     height, width = frame.shape[:2]
#     frame_center = (width // 2, height // 2)

#     # Convert to grayscale for object detection
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Apply adaptive thresholding
#     thresh = cv2.adaptiveThreshold(
#         blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
#     )

#     # Use Canny edge detection
#     edges = cv2.Canny(blurred, 50, 150)

#     # Combine thresholding and edges
#     enhanced = cv2.addWeighted(thresh, 0.7, edges, 0.3, 0)

#     # Find contours
#     contours, _ = cv2.findContours(enhanced, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     closest_contour = None
#     min_distance = float('inf')

#     # Loop through contours to find the most relevant object
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         contour_center = (x + w // 2, y + h // 2)
#         distance = math.hypot(contour_center[0] - frame_center[0], contour_center[1] - frame_center[1])
#         area = w * h

#         # Focus on contours that are large enough and closest to the center
#         if area > 1000 and distance < min_distance:
#             min_distance = distance
#             closest_contour = (x, y, w, h)

#     # If a relevant contour is found, process it
#     if closest_contour:
#         x, y, w, h = closest_contour

#         # Calculate the center point
#         center_x, center_y = x + w // 2, y + h // 2

#         # Convert dimensions to real-world measurements
#         real_width = w * RATIO
#         real_height = h * RATIO

#         # Draw the bounding box
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Draw the center point
#         cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

#         # Display the center point and dimensions
#         cv2.putText(frame, f"Center: ({center_x}, {center_y})", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#         cv2.putText(frame, f"L: {real_height:.2f}cm, W: {real_width:.2f}cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#     # Show the frame
#     cv2.imshow("ESP32-CAM Object Measurement", frame)

#     # Break the loop if the 'Esc' key is pressed
#     key = cv2.waitKey(1)
#     if key == 27:
#         break

# # Release resources
# cv2.destroyAllWindows()

# scripts/authomatic.py
import cv2
import math
import numpy as np
import requests
import time

ESP32_URL = "http://192.168.160.11/stream"
RATIO = 15 / 206
RESOLUTION = (640, 480)  # Set the desired resolution (width, height)

def get_esp32_frame():
    try:
        stream = requests.get(ESP32_URL, stream=True, timeout=2)
        byte_data = b""
        for chunk in stream.iter_content(chunk_size=4096):
            byte_data += chunk
            a = byte_data.find(b'\xff\xd8')
            b = byte_data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = byte_data[a:b+2]
                byte_data = byte_data[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                # Resize the frame to the desired resolution
                frame_resized = cv2.resize(frame, RESOLUTION)
                return frame_resized
    except:
        return None

def process_video(placeholder):
    while True:
        frame = get_esp32_frame()
        if frame is None:
            time.sleep(1)
            continue

        height, width = frame.shape[:2]
        frame_center = (width // 2, height // 2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        edges = cv2.Canny(blurred, 50, 150)
        enhanced = cv2.addWeighted(thresh, 0.7, edges, 0.3, 0)
        contours, _ = cv2.findContours(enhanced, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        closest_contour = None
        min_distance = float('inf')

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            contour_center = (x + w // 2, y + h // 2)
            distance = math.hypot(contour_center[0] - frame_center[0], contour_center[1] - frame_center[1])
            if area > 1000 and distance < min_distance:
                min_distance = distance
                closest_contour = (x, y, w, h)

        if closest_contour:
            x, y, w, h = closest_contour
            center_x, center_y = x + w // 2, y + h // 2
            real_width = w * RATIO
            real_height = h * RATIO
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
            cv2.putText(frame, f"Center: ({center_x}, {center_y})", (x, y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"L: {real_height:.2f}cm, W: {real_width:.2f}cm", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        placeholder.image(frame_rgb, channels="RGB")


# import cv2
# import math
# import numpy as np
# import requests
# import time

# ESP32_URL = "/stream"  # Update with your ESP32 stream URL
# RATIO = 15 / 290        # Real-world cm per pixel
# RESOLUTION = (640, 480) # Frame resolution

# def get_esp32_frame():
#     try:
#         stream = requests.get(ESP32_URL, stream=True, timeout=2)
#         byte_data = b""
#         for chunk in stream.iter_content(chunk_size=4096):
#             byte_data += chunk
#             a = byte_data.find(b'\xff\xd8')
#             b = byte_data.find(b'\xff\xd9')
#             if a != -1 and b != -1:
#                 jpg = byte_data[a:b+2]
#                 byte_data = byte_data[b+2:]
#                 frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                 return cv2.resize(frame, RESOLUTION)
#     except:
#         return None

# def process_video(placeholder):
#     while True:
#         frame = get_esp32_frame()
#         if frame is None:
#             time.sleep(1)
#             continue

#         height, width = frame.shape[:2]
#         frame_center = (width // 2, height // 2)

#         # --- Preprocessing ---
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Apply CLAHE for lighting normalization
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#         gray = clahe.apply(gray)

#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#         thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                        cv2.THRESH_BINARY_INV, 11, 2)
#         edges = cv2.Canny(blurred, 50, 150)
#         enhanced = cv2.addWeighted(thresh, 0.7, edges, 0.3, 0)

#         # Morphological closing to remove small gaps and noise
#         kernel = np.ones((3, 3), np.uint8)
#         morphed = cv2.morphologyEx(enhanced, cv2.MORPH_CLOSE, kernel, iterations=2)

#         contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         closest_contour = None
#         min_distance = float('inf')

#         for contour in contours:
#             x, y, w, h = cv2.boundingRect(contour)
#             area = w * h
#             contour_center = (x + w // 2, y + h // 2)
#             distance = math.hypot(contour_center[0] - frame_center[0], contour_center[1] - frame_center[1])

#             # Skip if too small
#             if area < 1000:
#                 continue

#             # Skip dark regions (likely shadows)
#             mean_intensity = cv2.mean(gray[y:y+h, x:x+w])[0]
#             if mean_intensity < 40:
#                 continue

#             # Find the closest valid object to center
#             if distance < min_distance:
#                 min_distance = distance
#                 closest_contour = (x, y, w, h)

#         if closest_contour:
#             x, y, w, h = closest_contour
#             center_x, center_y = x + w // 2, y + h // 2
#             real_width = w * RATIO
#             real_height = h * RATIO

#             # Draw results
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
#             cv2.putText(frame, f"Center: ({center_x}, {center_y})", (x, y - 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#             cv2.putText(frame, f"L: {real_height:.2f}cm, W: {real_width:.2f}cm", (x, y - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#         # Show in Streamlit
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         placeholder.image(frame_rgb, channels="RGB")
