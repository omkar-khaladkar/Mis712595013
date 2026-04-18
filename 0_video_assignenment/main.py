import random
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ---------------- CONFIG ----------------
INPUT_VIDEO = "input.mp4"
OUTPUT_VIDEO = "output.mp4"
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FONT_SIZE_MAIN = 40
FONT_SIZE_NAME = 30
FONT_PATH = "C:/Windows/Fonts/arial.ttf"
# --------------------------------------

# Load input video
video = mp.VideoFileClip(INPUT_VIDEO)
DURATION = video.duration

# Resize input video
video_resized = video.resize(width=VIDEO_WIDTH)
video_resized = video_resized.set_position(("center", 0))

# Create black background
background = mp.ColorClip(
    size=(VIDEO_WIDTH, VIDEO_HEIGHT),
    color=(0, 0, 0),
    duration=DURATION
)

# -------- Function to create text image clip --------
def create_text_clip(text, fontsize, color="white", duration=1, position=("center", VIDEO_HEIGHT - 60)):
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, fontsize)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    if position == "center":
        x = (VIDEO_WIDTH - text_width) // 2
        y = (VIDEO_HEIGHT - text_height) // 2
    elif isinstance(position, tuple):
        x, y = position
    else:
        x = 0
        y = 0

    draw.text((x, y), text, fill=color, font=font)
    return mp.ImageClip(np.array(img)).set_duration(duration)

# Bottom ribbon text (continuous)
bottom_text = create_text_clip(
    "Python Assignment version 0",
    FONT_SIZE_MAIN,
    duration=DURATION,
    position=((VIDEO_WIDTH // 2) - 250, VIDEO_HEIGHT - 60)
)

# Random moving name text
name_clips = []
interval = 1  # change position every 1 second

for t in range(int(DURATION)):
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE_NAME)

    x = random.randint(0, VIDEO_WIDTH - 300)
    y = random.randint(0, VIDEO_HEIGHT - 150)

    draw.text((x, y), "Mangesh Chavan", fill="red", font=font)
    name_clip = mp.ImageClip(np.array(img)).set_start(t).set_duration(interval)
    name_clips.append(name_clip)

# Composite everything
final_video = mp.CompositeVideoClip(
    [background, video_resized, bottom_text] + name_clips,
    size=(VIDEO_WIDTH, VIDEO_HEIGHT)
)

# Export
final_video.write_videofile(
    OUTPUT_VIDEO,
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
