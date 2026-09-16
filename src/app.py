from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import shutil, uuid, os, tempfile

# Ensure the src folder is in the path for imports
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion import prepare_frame
from mesh import get_landmarks
from math_engine import calculate_golden_ratio, calculate_fwhr, calculate_symmetry
from visualize import overlay_results

app = FastAPI()
TEMP_DIR = tempfile.gettempdir()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # 1. Save uploaded file temporarily
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 2. Run the Aphrodite Engine
    frame = prepare_frame(temp_path)
    if frame is None:
        return JSONResponse(status_code=400, content={"error": "corrupt or invalid image"})
        
    landmarks = get_landmarks(frame)
    if landmarks is None:
        os.remove(temp_path)
        return JSONResponse(status_code=422, content={"error": "no face detected"})

    # 3. Calculate Math
    g_ratio, g_variance = calculate_golden_ratio(landmarks)
    fwhr = calculate_fwhr(landmarks)
    symmetry = calculate_symmetry(landmarks)

    result = {
        "golden_ratio": g_ratio,
        "fwhr": fwhr,
        "symmetry": symmetry
    }

    # 4. Generate Visualization
    output_path = os.path.join(TEMP_DIR, f"annotated_{uuid.uuid4()}.jpg")
    overlay_results(frame, landmarks, result, output_path)

    # 5. Cleanup and Respond
    os.remove(temp_path)
    return {"scores": result, "annotated_image_url": f"/result/{os.path.basename(output_path)}"}

@app.get("/result/{filename}")
def get_result(filename: str):
    return FileResponse(os.path.join(TEMP_DIR, filename))
