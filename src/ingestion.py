import cv2
import os

def prepare_frame(image_path, max_edge=720):
    """Loads, resizes, and converts an image from BGR to RGB."""
    # 1. Check if file exists
    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return None
    
    # 2. Read image (OpenCV loads as BGR by default)
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Could not decode image. It might be corrupted: {image_path}")
        return None

    # 3. Get current dimensions
    h, w = img.shape[:2]
    
    # 4. Resize if the longest edge is larger than max_edge to save memory
    if max(h, w) > max_edge:
        scale = max_edge / float(max(h, w))
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # 5. Convert BGR (OpenCV) to RGB (MediaPipe requirement)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img_rgb
