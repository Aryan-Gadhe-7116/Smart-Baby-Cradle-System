import cv2
import time
import math
from ultralytics import YOLO

# Load AI model
model = YOLO("yolov8n.pt")

# Open webcam automatically
# Connect only to external USB webcam
camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("External USB webcam not found!")
    exit()

print("External USB Webcam Connected Successfully")

# Cradle boundary (normalized coordinates)
# Adjust these values once according to webcam placement.
x1, y1 = 0.15, 0.15
x2, y2 = 0.85, 0.90

previous_center = None
last_movement_time = time.time()

while True:

    success, frame = camera.read()

    if not success:
        break

    height, width, _ = frame.shape

    # Convert normalized boundary to pixels
    left = int(x1 * width)
    top = int(y1 * height)
    right = int(x2 * width)
    bottom = int(y2 * height)

    # Draw cradle monitoring area
    cv2.rectangle(
        frame,
        (left, top),
        (right, bottom),
        (255, 0, 0),
        2
    )

    # Detect objects
    results = model(frame, conf=0.40, verbose=False)

    baby_detected = False
    current_center = None

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])

            # COCO class 0 = person
            if class_id == 0:

                bx1, by1, bx2, by2 = map(
                    int, box.xyxy[0].tolist()
                )

                # Find center of detected person
                cx = (bx1 + bx2) // 2
                cy = (by1 + by2) // 2

                # Check if person is inside cradle area
                if left < cx < right and top < cy < bottom:

                    baby_detected = True
                    current_center = (cx, cy)

                    cv2.rectangle(
                        frame,
                        (bx1, by1),
                        (bx2, by2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        "PERSON DETECTED",
                        (bx1, by1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

    # Detect movement between frames
    movement = False

    if current_center is not None:

        if previous_center is not None:

            distance = math.dist(
                current_center,
                previous_center
            )

            if distance > 15:
                movement = True
                last_movement_time = time.time()

        previous_center = current_center

    else:
        previous_center = None

    # Display status
    if not baby_detected:
        status = "NOT DETECTED IN MONITORING AREA"

    elif movement:
        status = "MOVEMENT DETECTED"

    else:
        status = "PERSON DETECTED"

    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0) if baby_detected else (0, 0, 255),
        2
    )

    cv2.imshow(
        "Baby Cradle Monitoring System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()