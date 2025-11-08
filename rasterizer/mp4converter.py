import cv2
import os

# Folder containing your BMP frames
frames_dir = "images"

# Collect and sort all BMP filenames
frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".bmp")])

if not frames:
    raise ValueError("No BMP files found in folder!")

# Load the first frame to get video size
first_frame_path = os.path.join(frames_dir, frames[0])
first_frame = cv2.imread(first_frame_path)
height, width, _ = first_frame.shape

# Output video writer
out = cv2.VideoWriter(
    "output.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),  # Codec (mp4v = standard H.264)
    30,  # Frames per second (change if needed)
    (width, height)
)

# Loop through all frames
for i, f in enumerate(frames):
    frame_path = os.path.join(frames_dir, f)
    frame = cv2.imread(frame_path)
    if frame is None:
        print(f"Skipping {f} (could not read)")
        continue
    out.write(frame)
    if i % 100 == 0:
        print(f"Processed {i}/{len(frames)} frames...")

out.release()
print("Video saved as output.mp4")