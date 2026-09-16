import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

LANDMARK_MAP = {
    "hairline": 10,
    "chin": 152,
    "left_cheek": 234,
    "right_cheek": 454,
    "brow_mid": 9,
    "upper_lip": 0,
    "nose_tip": 1,
    "left_mouth": 61,
    "right_mouth": 291,
    "left_eye": 33,
    "right_eye": 263
}

def get_landmarks(img_rgb):
    if img_rgb is None:
        return None

    h, w = img_rgb.shape[:2]
    
    # 1. Setup the modern Tasks API Options
    base_options = python.BaseOptions(model_asset_path='assets/face_landmarker.task')
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        num_faces=1
    )
    
    # 2. Run the detector
    with vision.FaceLandmarker.create_from_options(options) as detector:
        # Convert standard numpy array to MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        detection_result = detector.detect(mp_image)
        
        if not detection_result.face_landmarks:
            print("[ERROR] No face detected in the image.")
            return None
            
        face = detection_result.face_landmarks[0]
        
        # 3. Extract named coordinates
        named_landmarks = {}
        for name, idx in LANDMARK_MAP.items():
            landmark = face[idx]
            px_x = int(landmark.x * w)
            px_y = int(landmark.y * h)
            named_landmarks[name] = (px_x, px_y)
            
        return named_landmarks
