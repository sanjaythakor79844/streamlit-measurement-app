# import streamlit as st
# import scripts.automatic as authomatic
# import scripts.manual as page1
# import scripts.counting as test2

# st.set_page_config(
#     page_title="Object Measurement & Counting System",
#     page_icon="📏",
#     layout="wide"
# )

# # Initialize session state
# st.session_state.setdefault("video_running", False)
# st.session_state.setdefault("object_count", 0)
# st.session_state.setdefault("selected_mode", "Automatic Object Measurement")

# # App Header
# st.markdown(
#     """
#     <h1 style="text-align:center; color:#4CAF50;">
#         📏 Object Measurement & Counting System
#     </h1>
#     <hr style="margin-top:-10px;">
#     """, unsafe_allow_html=True
# )

# # Sidebar - Control Panel
# st.sidebar.title("🧭 Control Panel")

# available_modes = [
#     "Automatic Object Measurement",
#     "Manual Object Measurement",
#     "Object Counting (Background Subtraction)"
# ]

# selected_script = st.sidebar.selectbox(
#     "🛠 Select Functionality",
#     available_modes,
#     index=available_modes.index(st.session_state.selected_mode)
# )
# st.session_state.selected_mode = selected_script

# # Start and Stop buttons
# col1, col2 = st.sidebar.columns(2)
# with col1:
#     if not st.session_state.video_running:
#         if st.button("▶ Start"):
#             st.session_state.video_running = True
# with col2:
#     if st.session_state.video_running:
#         if st.button("⏹ Stop"):
#             st.session_state.video_running = False
#             st.rerun()

# # Reset Button (for counting)
# if selected_script == "Object Counting (Background Subtraction)" and st.session_state.video_running:
#     if st.sidebar.button("🔄 Reset Count"):
#         test2.reset_count()  # Call reset_count function to reset the count

# # Instructions
# with st.sidebar.expander("📘 How to Use", expanded=True):
#     if selected_script == "Automatic Object Measurement":
#         st.markdown("""1. Click **Start** to begin live measurement. 2. Objects will be automatically detected and measured. 3. Press **Stop** to end the session.""")
#     elif selected_script == "Manual Object Measurement":
#         st.markdown("""1. Click **Start** to begin the stream. 2. Select points manually for object dimensions. 3. Press **Stop** to reset and start new session.""")
#     elif selected_script == "Object Counting (Background Subtraction)":
#         st.markdown("""1. Click **Start** to begin counting. 2. Items crossing the detection line will be counted. 3. Press **Stop** to finish and reset the count.""")

# # Main layout
# st.markdown("### 🔍 Live Video Feed")
# video_placeholder = st.empty()
# stats_placeholder = st.empty()  # New placeholder for stats

# if st.session_state.video_running:
#     if selected_script == "Automatic Object Measurement":
#         authomatic.process_video(video_placeholder)
#     elif selected_script == "Manual Object Measurement":
#         page1.process_video(video_placeholder)
#     elif selected_script == "Object Counting (Background Subtraction)":
#         # Pass both video_placeholder and stats_placeholder
#         test2.process_video(video_placeholder, stats_placeholder)
# else:
#     st.info("📡 Click 'Start' in the sidebar to begin streaming from the ESP32-CAM.")


import streamlit as st
import scripts.automatic as authomatic
import scripts.manual as page1
import scripts.counting as test2

st.set_page_config(
    page_title="Object Measurement & Counting System",
    page_icon="📏",
    layout="wide"
)

# Initialize session state
st.session_state.setdefault("video_running", False)
st.session_state.setdefault("object_count", 0)
st.session_state.setdefault("selected_mode", "Automatic Object Measurement")

# App Header
st.markdown(
    """
    <h1 style="text-align:center; color:#4CAF50;">
        📏 Object Measurement & Counting System
    </h1>
    <hr style="margin-top:-10px;">
    """, unsafe_allow_html=True
)

# Sidebar - Control Panel
st.sidebar.title("🧭 Control Panel")

available_modes = [
    "Automatic Object Measurement",
    "Manual Object Measurement",
    "Object Counting (Background Subtraction)"
]

selected_script = st.sidebar.selectbox(
    "🛠 Select Functionality",
    available_modes,
    index=available_modes.index(st.session_state.selected_mode)
)
st.session_state.selected_mode = selected_script

# Start and Stop buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if not st.session_state.video_running:
        if st.button("▶ Start"):
            st.session_state.video_running = True
with col2:
    if st.session_state.video_running:
        if st.button("⏹ Stop"):
            st.session_state.video_running = False
            st.experimental_rerun()

# Reset Button (for counting)
if selected_script == "Object Counting (Background Subtraction)" and st.session_state.video_running:
    if st.sidebar.button("🔄 Reset Count"):
        test2.reset_count()  # Make sure test2 has this function

# Instructions
with st.sidebar.expander("📘 How to Use", expanded=True):
    if selected_script == "Automatic Object Measurement":
        st.markdown("""1. Click **Start** to begin live measurement. 2. Objects will be automatically detected and measured. 3. Press **Stop** to end the session.""")
    elif selected_script == "Manual Object Measurement":
        st.markdown("""1. Click **Start** to begin the stream. 2. Select points manually for object dimensions. 3. Press **Stop** to reset and start new session.""")
    elif selected_script == "Object Counting (Background Subtraction)":
        st.markdown("""1. Click **Start** to begin counting. 2. Items crossing the detection line will be counted. 3. Press **Stop** to finish and reset the count.""")

# Main layout
st.markdown("### 🔍 Live Video Feed")
video_placeholder = st.empty()
stats_placeholder = st.empty()  # For future use

if st.session_state.video_running:
    if selected_script == "Automatic Object Measurement":
        authomatic.process_video(video_placeholder)
    elif selected_script == "Manual Object Measurement":
        page1.process_video(video_placeholder)
    elif selected_script == "Object Counting (Background Subtraction)":
        test2.process_video(video_placeholder, stats_placeholder)
else:
    st.info("📡 Click 'Start' in the sidebar to begin streaming from the ESP32-CAM.")
