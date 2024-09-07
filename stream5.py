import streamlit as st
import numpy as np
import cv2
import tempfile
import pandas as pd

# Function to generate a dummy video
def generate_dummy_video(file_path, num_frames=100, width=640, height=480):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(file_path, fourcc, 20.0, (width, height))

    for _ in range(num_frames):
        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        cv2.putText(frame, "Front Row: {}".format(np.random.randint(0, 5)), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "Back Row: {}".format(np.random.randint(0, 5)), (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "Age Group: {}".format(np.random.choice(['0-18', '19-35', '36-60', '60+'])), (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        out.write(frame)

    out.release()

# Function to simulate detection of people
def detect_people(video_path):
    video = cv2.VideoCapture(video_path)
    frame_counts = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create lists to hold the detected counts
    front_row_counts = []
    back_row_counts = []
    age_groups = {'0-18': 0, '19-35': 0, '36-60': 0, '60+': 0}

    for _ in range(frame_counts):
        ret, frame = video.read()
        if not ret:
            break
        
        # Simulate detection counts from frame text
        front_row_count = np.random.randint(0, 5)
        back_row_count = np.random.randint(0, 5)
        age_group = np.random.choice(['0-18', '19-35', '36-60', '60+'])
        
        front_row_counts.append(front_row_count)
        back_row_counts.append(back_row_count)
        age_groups[age_group] += 1

    video.release()
    
    # Convert age group counts to DataFrame
    age_group_df = pd.DataFrame(list(age_groups.items()), columns=['Age Group', 'Count'])
    
    return front_row_counts, back_row_counts, age_group_df

# Main Streamlit application
def main():
    st.title('Bus People Detection')

    # Generate a dummy video file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        generate_dummy_video(temp_file.name)
        video_path = temp_file.name

    st.video(video_path)  # Display the video in Streamlit

    if st.button('Detect People'):
        front_row_counts, back_row_counts, age_group_df = detect_people(video_path)
        
        if front_row_counts and back_row_counts:
            # Create DataFrames for counts
            df_counts = pd.DataFrame({
                'Frame Number': range(len(front_row_counts)),
                'Front Row Count': front_row_counts,
                'Back Row Count': back_row_counts
            })
            
            st.write("Detected People Counts:")
            st.write(df_counts)
            
            st.write("Age Group Distribution:")
            st.write(age_group_df)
            
            # Plot counts over frames
            st.line_chart(df_counts.set_index('Frame Number')[['Front Row Count', 'Back Row Count']])
            st.bar_chart(age_group_df.set_index('Age Group'))
        else:
            st.write("No people detected or error in detection.")

if __name__ == "__main__":
    main()
