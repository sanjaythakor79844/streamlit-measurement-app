# import cv2
# import math
# import requests
# import numpy as np

# # List to store clicked points and measured distances
# points = []
# measured_distances = []
# product_count = 0

# # Ratio for converting pixel measurements to centimeters
# ratio = 15 / 120

# # ESP32-CAM stream URL (replace with your ESP32 IP address)
# ESP32_URL = "http://192.168.25.11:81/stream"  # Replace with your ESP32-CAM IP

# def get_esp32_frame():
#     """Fetch a frame from ESP32-CAM MJPEG stream."""
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

# # Mouse callback function for capturing points
# def point(event, x, y, flags, param):
#     global points
#     if event == cv2.EVENT_LBUTTONDOWN:
#         points.append((x, y))

# # Create a window and set mouse callback
# cv2.namedWindow("Object Measurement System")
# cv2.setMouseCallback("Object Measurement System", point)

# # Main loop to capture and process frames
# while True:
#     frame = get_esp32_frame()
#     if frame is None:
#         continue  # Skip if no frame received

#     # Draw circles on clicked points
#     for pt in points:
#         cv2.circle(frame, pt, 5, (0, 0, 255), -1)
    
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('z') and len(points) > 1:
#         new_distances = []
#         x_values = [pt[0] for pt in points]
#         y_values = [pt[1] for pt in points]

#         # Calculate width and height in pixels
#         width_px = max(x_values) - min(x_values)
#         height_px = max(y_values) - min(y_values)

#         # Convert to real-world measurements (in cm)
#         width_cm = width_px * ratio
#         height_cm = height_px * ratio

#         # Display measured dimensions on the frame
#         print(f"Product {product_count + 1}: Width = {width_cm:.2f} cm, Height = {height_cm:.2f} cm")
        
#         # Calculate and store distances between points
#         for i in range(len(points) - 1):
#             pt1, pt2 = points[i], points[i + 1]
#             dist_px = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
#             dist_cm = dist_px * ratio
#             new_distances.append((pt1, pt2, dist_cm))

#         measured_distances.extend(new_distances)
#         points.clear()  # Clear points after measurement

#     if key == ord('n'):
#         points.clear()
#         measured_distances.clear()
#         product_count += 1

#     # Draw lines and distances between points
#     for pt1, pt2, dist in measured_distances:
#         cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
#         mid_x, mid_y = (pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2
#         cv2.putText(frame, f"{dist:.2f} cm", (mid_x, mid_y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

#     # Display product count
#     cv2.putText(frame, f"Product Count: {product_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

#     # Show the frame
#     cv2.imshow("Object Measurement System", frame)

#     if key == 27:  # 'Esc' to exit
#         break

# cv2.destroyAllWindows()

# # # # # scripts/page1.py 
# # # import cv2
# # # import math
# # # import requests
# # # import numpy as np

# # # # List to store clicked points and measured distances
# # # points = []
# # # measured_distances = []
# # # product_count = 0

# # # # Ratio for converting pixel measurements to centimeters
# # # ratio = 15 / 290

# # # # ESP32-CAM stream URL (replace with your ESP32 IP address)
# # # ESP32_URL = "http://192.168.25.11:81/stream"  # Replace with your ESP32-CAM IP

# # # def get_esp32_frame():
# # #     """Fetch a frame from ESP32-CAM MJPEG stream."""
# # #     try:
# # #         stream = requests.get(ESP32_URL, stream=True, timeout=2)
# # #         byte_data = b""
        
# # #         for chunk in stream.iter_content(chunk_size=4096):
# # #             byte_data += chunk
# # #             a = byte_data.find(b'\xff\xd8')  # Start of JPEG
# # #             b = byte_data.find(b'\xff\xd9')  # End of JPEG
            
# # #             if a != -1 and b != -1:
# # #                 jpg = byte_data[a:b+2]
# # #                 byte_data = byte_data[b+2:]
# # #                 frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
# # #                 return frame
# # #     except requests.exceptions.RequestException as e:
# # #         print("⚠️ Error: Could not connect to ESP32-CAM", e)
# # #         return None

# # # # Mouse callback function for capturing points
# # # def point(event, x, y, flags, param):
# # #     global points
# # #     if event == cv2.EVENT_LBUTTONDOWN:
# # #         points.append((x, y))

# # # # Main function to process video frames
# # # def process_video(placeholder):
# # #     global points, measured_distances, product_count

# # #     cv2.namedWindow("Object Measurement System")
# # #     cv2.setMouseCallback("Object Measurement System", point)

# # #     while True:
# # #         frame = get_esp32_frame()
# # #         if frame is None:
# # #             continue  # Skip if no frame received

# # #         # Draw circles on clicked points
# # #         for pt in points:
# # #             cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        
# # #         key = cv2.waitKey(1) & 0xFF
# # #         if key == ord('z') and len(points) > 1:
# # #             new_distances = []
# # #             x_values = [pt[0] for pt in points]
# # #             y_values = [pt[1] for pt in points]

# # #             # Calculate width and height in pixels
# # #             width_px = max(x_values) - min(x_values)
# # #             height_px = max(y_values) - min(y_values)

# # #             # Convert to real-world measurements (in cm)
# # #             width_cm = width_px * ratio
# # #             height_cm = height_px * ratio

# # #             # Display measured dimensions on the frame
# # #             print(f"Product {product_count + 1}: Width = {width_cm:.2f} cm, Height = {height_cm:.2f} cm")
            
# # #             # Calculate and store distances between points
# # #             for i in range(len(points) - 1):
# # #                 pt1, pt2 = points[i], points[i + 1]
# # #                 dist_px = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
# # #                 dist_cm = dist_px * ratio
# # #                 new_distances.append((pt1, pt2, dist_cm))

# # #             measured_distances.extend(new_distances)
# # #             points.clear()  # Clear points after measurement

# # #         if key == ord('n'):
# # #             points.clear()
# # #             measured_distances.clear()
# # #             product_count += 1

# # #         # Draw lines and distances between points
# # #         for pt1, pt2, dist in measured_distances:
# # #             cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
# # #             mid_x, mid_y = (pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2
# # #             cv2.putText(frame, f"{dist:.2f} cm", (mid_x, mid_y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

# # #         # Display product count
# # #         cv2.putText(frame, f"Product Count: {product_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

# # #         # Show the frame
# # #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #         frame_resized = cv2.resize(frame_rgb, (640, 480))  # Larger display size
# # #         placeholder.image(frame_resized, channels="RGB") 

# # #         if key == 27: 
# # #             break

# # #     cv2.destroyAllWindows()
import streamlit as st
import cv2
import numpy as np
import math
import csv
import os
import urllib.request
from PIL import Image
from streamlit_drawable_canvas import st_canvas

def process_video(video_placeholder):
    # Constants
    ESP32_CAM_URL = "http://192.168.160.11/stream"
    DEFAULT_RATIO = 15 / 273.03
    CSV_FILENAME = "measurements.csv"
    MAX_DISPLAY_WIDTH = 800  # Optional: limit frame width for display

    # Initialize CSV file if it doesn't exist
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Product Number", "Width (cm)", "Height (cm)", "Distances (cm)"])

    # Initialize session state
    st.session_state.setdefault("points", [])
    st.session_state.setdefault("measured_distances", [])
    st.session_state.setdefault("product_count", 0)
    st.session_state.setdefault("captured_image", None)
    st.session_state.setdefault("ratio", None)
    st.session_state.setdefault("calibration_mode", False)

    st.info("""Steps: 
    1. Capture frame. 
    2. Toggle calibration mode and select 2 points to calibrate.
    3. Measure distances and save.""")

    if st.button("Start New Product"):
        st.session_state.points = []
        st.session_state.measured_distances = []
        st.session_state.product_count += 1
        st.session_state.captured_image = None

    st.session_state.calibration_mode = st.checkbox("🛠 Enable Calibration Mode", value=st.session_state.calibration_mode)

    manual_ratio = st.number_input("Manual ratio (cm/pixel):", min_value=0.0001,
                                   value=st.session_state.ratio if st.session_state.ratio else DEFAULT_RATIO,
                                   step=0.0001, format="%.4f")
    use_manual = st.checkbox("✅ Use manual ratio instead")
    if use_manual:
        st.session_state.ratio = manual_ratio

    st.markdown("### 🎥 Stream Preview")
    frame_placeholder = st.empty()

    # Stream grabber with timeout
    def get_frame_from_stream(url, timeout=5):
        try:
            stream = urllib.request.urlopen(url, timeout=timeout)
            bytes_data = b""
            while True:
                bytes_data += stream.read(1024)
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    img_np = np.frombuffer(jpg, dtype=np.uint8)
                    frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
                    return frame
        except Exception as e:
            st.error(f"Error reading from stream: {e}")
            return None

    if st.button("📸 Capture Frame"):
        frame = get_frame_from_stream(ESP32_CAM_URL)
        if frame is not None:
            # Resize if too large for display
            height, width = frame.shape[:2]
            if width > MAX_DISPLAY_WIDTH:
                scale_ratio = MAX_DISPLAY_WIDTH / width
                new_dim = (MAX_DISPLAY_WIDTH, int(height * scale_ratio))
                frame = cv2.resize(frame, new_dim, interpolation=cv2.INTER_AREA)
            st.session_state.captured_image = frame
            video_placeholder.image(frame, caption="Captured Frame", channels="BGR")

    if st.session_state.captured_image is not None:
        img = st.session_state.captured_image.copy()
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=3,
            stroke_color="#FF0000",
            background_image=img_pil,
            height=img.shape[0],
            width=img.shape[1],
            drawing_mode="point",
            key="manual-canvas"
        )

        if canvas_result.json_data:
            st.session_state.points = [(int(obj["left"]), int(obj["top"])) for obj in canvas_result.json_data["objects"]]

        if st.session_state.calibration_mode:
            if len(st.session_state.points) == 2:
                known_cm = st.number_input("Real-world distance (cm):", min_value=0.1, value=15.0)
                pt1, pt2 = st.session_state.points
                pixel_dist = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
                if pixel_dist > 0:
                    st.session_state.ratio = known_cm / pixel_dist
                    st.success(f"Calibration complete: {st.session_state.ratio:.4f} cm/pixel")
            else:
                st.warning("Please select exactly 2 points for calibration.")
        else:
            ratio = st.session_state.ratio or DEFAULT_RATIO
            img_copy = img.copy()
            distances = []

            for i in range(len(st.session_state.points) - 1):
                pt1, pt2 = st.session_state.points[i], st.session_state.points[i + 1]
                cv2.line(img_copy, pt1, pt2, (0, 255, 0), 2)
                dist_px = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
                dist_cm = dist_px * ratio
                distances.append(dist_cm)
                mid = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
                cv2.putText(img_copy, f"{dist_cm:.2f} cm", mid, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            st.session_state.measured_distances = distances
            frame_placeholder.image(img_copy, caption="Measured Image", channels="BGR")

    if st.button("💾 Measure & Save"):
        if len(st.session_state.points) > 1 and st.session_state.ratio:
            x_vals = [pt[0] for pt in st.session_state.points]
            y_vals = [pt[1] for pt in st.session_state.points]
            width_px = max(x_vals) - min(x_vals)
            height_px = max(y_vals) - min(y_vals)
            width_cm = width_px * st.session_state.ratio
            height_cm = height_px * st.session_state.ratio

            with open(CSV_FILENAME, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([st.session_state.product_count + 1,
                                 f"{width_cm:.2f}", f"{height_cm:.2f}",
                                 ", ".join([f"{d:.2f}" for d in st.session_state.measured_distances])])

            st.success(f"✅ Measurements saved for Product {st.session_state.product_count + 1}")
            st.session_state.points = []
            st.session_state.captured_image = None
            st.session_state.measured_distances = []

    # Add a CSV download button
    if os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, "rb") as file:
            st.download_button(
                label="⬇️ Download Measurements CSV",
                data=file,
                file_name=CSV_FILENAME,
                mime="text/csv",
            )

    # Optional: Display Streamlit version info for debugging
    st.caption(f"Running on Streamlit version {st.__version__}")
