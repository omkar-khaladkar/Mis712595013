import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import math
import os

# ------------------ Setup ------------------
video_path = "sample.mp4"  # CHANGE THIS
output_csv = "driver_expression_output.csv"

if not os.path.exists(video_path):
    print("❌ Video file not found. Check path:", video_path)
    exit()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Cannot open video file.")
    exit()

data = []

# ------------------ Helper Functions ------------------
def eye_aspect_ratio(landmarks, eye_indices, w, h):
    pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]
    A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    ear = (A + B) / (2.0 * C)
    return ear

def pupil_position(landmarks, eye_indices, iris_indices, w, h):
    eye_pts = np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in eye_indices])
    iris_pts = np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in iris_indices])

    eye_center_x = np.mean(eye_pts[:, 0])
    iris_center_x = np.mean(iris_pts[:, 0])

    if iris_center_x < eye_center_x - 5:
        return "Left"
    elif iris_center_x > eye_center_x + 5:
        return "Right"
    else:
        return "Center"

def get_head_pose(landmarks, w, h):
    model_points = np.array([
        (0.0, 0.0, 0.0),         # Nose tip
        (0.0, -330.0, -65.0),   # Chin
        (-225.0, 170.0, -135.0),# Left eye left corner
        (225.0, 170.0, -135.0), # Right eye right corner
        (-150.0, -150.0, -125.0),# Left Mouth corner
        (150.0, -150.0, -125.0) # Right mouth corner
    ])

    image_points = np.array([
        (landmarks[1].x * w, landmarks[1].y * h),
        (landmarks[152].x * w, landmarks[152].y * h),
        (landmarks[263].x * w, landmarks[263].y * h),
        (landmarks[33].x * w, landmarks[33].y * h),
        (landmarks[287].x * w, landmarks[287].y * h),
        (landmarks[57].x * w, landmarks[57].y * h)
    ], dtype="double")

    focal_length = w
    center = (w / 2, h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs)

    rmat, _ = cv2.Rodrigues(rotation_vector)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    pitch, yaw, roll = angles
    return pitch, yaw, roll

def classify_head_rotation(yaw):
    if yaw > 40:
        return "Over Right Shoulder"
    elif yaw > 20:
        return "45Degree Right"
    elif yaw > -20:
        return "Center"
    elif yaw > -40:
        return "45Degree Left"
    else:
        return "Over Left Shoulder"

def classify_front_tilt(pitch):
    if pitch > 30:
        return "Extreme Back Tilt"
    elif pitch > 15:
        return "Back Tilt"
    elif pitch > -15:
        return "Straight Front Ahead"
    elif pitch > -30:
        return "Front Tilt"
    else:
        return "Extreme Front Tilt"

def classify_side_tilt(roll):
    if roll > 20:
        return "Head Top Right & Neck Left"
    elif roll < -20:
        return "Head Top Left & Neck Right"
    else:
        return "Straight"

def classify_driving_status(eye_state, head_rotation):
    if eye_state == "Closed":
        return "Distracted"
    elif head_rotation not in ["Center", "45Degree Right", "45Degree Left"]:
        return "Distracted"
    else:
        return "Focus"

# ------------------ Main Loop ------------------
frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("✅ End of video reached.")
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0].landmark

        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]
        left_iris_indices = [468, 469, 470, 471]
        right_iris_indices = [473, 474, 475, 476]

        left_ear = eye_aspect_ratio(face_landmarks, left_eye_indices, w, h)
        right_ear = eye_aspect_ratio(face_landmarks, right_eye_indices, w, h)
        avg_ear = (left_ear + right_ear) / 2

        eye_state = "Closed" if avg_ear < 0.22 else "Open"

        left_pupil = pupil_position(face_landmarks, left_eye_indices, left_iris_indices, w, h)
        right_pupil = pupil_position(face_landmarks, right_eye_indices, right_iris_indices, w, h)
        pupil_position_avg = left_pupil if left_pupil == right_pupil else "Center"

        pitch, yaw, roll = get_head_pose(face_landmarks, w, h)
        head_rotation = classify_head_rotation(yaw)
        head_front_tilt = classify_front_tilt(pitch)
        head_side_tilt = classify_side_tilt(roll)

        driving_status = classify_driving_status(eye_state, head_rotation)

    else:
        eye_state = pupil_position_avg = driving_status = head_rotation = head_front_tilt = head_side_tilt = "No Face"

    data.append([
        frame_number,
        eye_state,
        pupil_position_avg,
        driving_status,
        head_rotation,
        head_front_tilt,
        head_side_tilt
    ])

    frame_number += 1

cap.release()

# ------------------ Save to CSV ------------------
columns = [
    "Frame",
    "Eye State",
    "Pupil Position",
    "Driving Status",
    "Head Rotation",
    "Head Front Tilt",
    "Head Side Tilt"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv(output_csv, index=False)

print("📁 CSV file created at:", os.path.abspath(output_csv))
print("📊 Total frames processed:", len(data))
