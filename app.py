import os
import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip

def invertFrame(frame):
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of orange in HSV
    lower_val = np.array([0, 50, 50])
    upper_val = np.array([20, 255, 255]) 

    # Threshold the HSV image - any green color will show up as white
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # if there are any white pixels on mask, sum will be > 0
    has_orange = np.sum(mask)
    if has_orange > 1000:
        return False
    
    else:
        return True

def getROI(frame, width, height):
    # Define the region of interest (ROI)
    if width == 1280 and height == 720:
        x, y, w, h = 555, 5, 35, 35
    
    elif width == 1670 and height == 705:
        x, y, w, h = 752, 4, 35, 35

    # Set ROI
    roi = frame[y:y+h, x:x+w]

    # cv2.imshow("ROI", roi)
    # cv2.waitKey(1)

    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    threshold, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Apply Gaussian blurring
    blurred = cv2.GaussianBlur(thresholded, (3,3), 0)

    if invertFrame(roi):
        return cv2.bitwise_not(blurred)

    else:
        return blurred

def saveScores(in_game_only, one_fps):
    # Load the video
    if in_game_only:
        cap = cv2.VideoCapture(r'C:\Users\coleb\dev\RL-score-timestamps\input\test2.mp4') # In-game only

    else:
        cap = cv2.VideoCapture(r'C:\Users\coleb\dev\RL-score-timestamps\input\20230128_pyyrosRL_1721499439.mp4') # Entire stream

    # Get the frame count
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f'Total frames in video: {frame_count}')

    # Define the region of interest (ROI)
    x, y, w, h = 555, 5, 35, 35 # 1280 x 720

    if one_fps:
        # Iterate over each 60th frame
        for i in range(0, frame_count, 60):  
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)

            ret, frame = cap.read()

            roi = getROI(frame)

            cv2.imwrite(f'scores/rlnum{30000 + i}.png', roi)

    else:  
        # Iterate over each frame
        for i in range(frame_count):
            ret, frame = cap.read()

            roi = getROI(frame)

            cv2.imwrite(f'scores/rlnum{1100000 + i}.png', roi)

    # Release the video
    cap.release()

def determineScoreChange(prev_score, score, game, consec_entries):
    changed = False

    if prev_score == score:
        consec_entries += 1

        if consec_entries == 5:
            changed = True

            if score == 10:
                changed = False 
                game = False

            elif score == 0:
                changed = False
                game = True

    else:
        consec_entries = 1

    return changed, game, consec_entries

def makeClip(video_file, time):
    # Load the video
    cap = cv2.VideoCapture(video_file) 

    # Get the frame count
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cap.release()

    # Set the start and end times of the desired portion of the video
    start_time = time - 10  # in seconds
    end_time = time + 10   # in seconds

    if start_time < 0:
        start_time = 0

    if end_time > int(frame_count / 60):
        end_time = int(frame_count / 60)

    # Load the video
    video = VideoFileClip(video_file)

    # Trim the video
    trimmed_video = video.subclip(start_time, end_time)

    try:
        output_directory
    except NameError:
        # Save the trimmed video
        trimmed_video.write_videofile(f'clips/{os.path.basename(video_file)[:-4]}_{time}.mp4')
    else:
        if output_directory == '':
            # Save the trimmed video
            trimmed_video.write_videofile(f'clips/{os.path.basename(video_file)[:-4]}_{time}.mp4')
        else:
            # Save the trimmed video
            trimmed_video.write_videofile(f'{output_directory}/{os.path.basename(video_file)[:-4]}_{time}.mp4')

def identifyScores(video):
    # Load the video
    cap = cv2.VideoCapture(video)

    # Get video resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Get the frame count
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    prev_score = None

    game = False

    consec_entries = 0

    timestamps = []

    # Load digit classifying model
    model = tf.keras.models.load_model('model')

    print(f'Total frames for {video}: {frame_count}')
    print(f'Frames per second: {fps}')

    if width == 1920 and height == 1080:
        # Iterate over each 60th frame
        for i in range(0, frame_count, 60):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()

            # Converts frame to 1280x720
            frame = cv2.resize(frame, (1280, 720))

            roi = getROI(frame, 1280, 720)

            score = np.argmax(model.predict(np.expand_dims(roi, axis = 0), verbose = 0)[0])

            changed, game, consec_entries = determineScoreChange(prev_score, score, game, consec_entries)

            if game == True and changed == True:
                sec = int(i / fps) - 5
                
                timestamps.append(sec)
            
            prev_score = score
        
    elif width == 1920 and height == 810:
        # Iterate over each 60th frame
        for i in range(0, frame_count, 60):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()

            # Converts frame to 1280x540
            frame = cv2.resize(frame, (1670, 705))

            roi = getROI(frame, 1670, 705)

            score = np.argmax(model.predict(np.expand_dims(roi, axis = 0), verbose = 0)[0])

            changed, game, consec_entries = determineScoreChange(prev_score, score, game, consec_entries)

            if game == True and changed == True:
                sec = int(i / fps) - 5
                
                timestamps.append(sec)
            
            prev_score = score     

    elif width == 1280 and height == 720:
        # Iterate over each 60th frame
        for i in range(0, frame_count, 60):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()

            roi = getROI(frame, width, height)

            score = np.argmax(model.predict(np.expand_dims(roi, axis = 0), verbose = 0)[0])

            changed, game, consec_entries = determineScoreChange(prev_score, score, game, consec_entries)

            if game == True and changed == True:
                sec = int(i / fps) - 5
                
                timestamps.append(sec)
            
            prev_score = score

    # Release the video
    cap.release()
    
    for timestamp in timestamps:
        makeClip(video, timestamp)

    print(f'Finished clipping {video}.')

# Create a GUI window
root = tk.Tk()

# Create a label to display instructions
label = tk.Label(root, text="Select one or more mp4 files:")
label.pack()

valid_files = False
file_paths = None

# Create a button that allows the user to browse and select files
def browseFiles():
    global browse_files_label
    
    try:
        browse_files_label
    except NameError:
        browse_files_label = None
    else:
        browse_files_label.destroy()

    global valid_files
    global file_paths

    file_paths = filedialog.askopenfilenames()

    if len(file_paths) != 0:
        valid_files = True

    for file_path in file_paths:
        if not file_path.endswith(".mp4"):
            message = f"Error: {file_path} is not an mp4 file."
            browse_files_label = tk.Label(root, text=message, fg="red")
            browse_files_label.pack()
            valid_files = False
            break

    if valid_files:
        message = "\n".join(file_paths)
        browse_files_label = tk.Label(root, text=f'Selected files:\n{message}')
        browse_files_label.pack()

    return 

browse_button = tk.Button(root, text="Browse", command=browseFiles)
browse_button.pack()

# Create label for space
tk.Label(root, text=" ").pack()

# Create a label to display instructions
label = tk.Label(root, text="Select clip output directory:")
label.pack()

def select_directory():
    global select_directory_label

    try:
        select_directory_label
    except NameError:
        select_directory_label = None
    else:
        select_directory_label.destroy()

    global output_directory
    output_directory = filedialog.askdirectory()

    message = output_directory
    select_directory_label = tk.Label(root, text=f'Output directory:\n{message}')
    select_directory_label.pack()

select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.pack()

# Create label for space
tk.Label(root, text=" ").pack()

def submit():
    if valid_files:
        for video in file_paths:
            identifyScores(video)

    else:
        message = f"Unable to process selected file(s)."
        error_label = tk.Label(root, text=message, fg="red")
        error_label.pack()

submit_button = tk.Button(root, text="Generate clips", command=submit)
submit_button.pack()

# Run the GUI window
root.mainloop()