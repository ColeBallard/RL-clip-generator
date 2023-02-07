import cv2
import pytesseract

# Load the video
cap = cv2.VideoCapture(r'C:\Users\coleb\dev\RL-score-timestamps\input\test2.mp4')

# Get the frame count
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f'Total frames in video: {frame_count}')

# Get the first frame
ret, prev_frame = cap.read()
prev_score = None

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the region of interest (ROI)
x, y, w, h = 555, 5, 35, 35

# Iterate over each frame
for i in range(0, frame_count, 60):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()

    M = cv2.getRotationMatrix2D((w // 2, h // 2), -4, 1.0)
    rotated = cv2.warpAffine(frame, M, (w, h))

    roi = rotated[y:y+h, x:x+w]

    cv2.imshow("ROI", rotated)
    if cv2.waitKey(1) == 13:
        break

    # # Convert to grayscale
    # gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # # Apply thresholding
    # threshold, thresholded = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    
    # # Apply Gaussian blurring
    # blurred = cv2.GaussianBlur(thresholded, (3,3), 0)
    
    # # Apply OCR to extract the text from the score displays
    # score = pytesseract.image_to_string(blurred, config='--psm 13')

    # if i == 0:
    #     print(f"Frame 0: Score is {score}") 
    
    # # Check if the score has changed
    # if prev_score is not None and score != prev_score:
    #     print(f"Frame {i}: Score changed to {score}")
    
    # prev_score = score

    # cv2.imshow("ROI", blurred)
    # if cv2.waitKey(1) == 13:
    #     break

# Release the video
cap.release()