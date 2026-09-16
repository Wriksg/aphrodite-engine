from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import shutil, uuid, os, tempfile, traceback
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
    try:
        temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        frame = prepare_frame(temp_path)
        if frame is None:
            return JSONResponse(status_code=400, content={"error": "corrupt or invalid image"})
            
        landmarks = get_landmarks(frame)
        if landmarks is None:
            os.remove(temp_path)
            return JSONResponse(status_code=422, content={"error": "no face detected"})

        g_ratio, g_variance = calculate_golden_ratio(landmarks)
        fwhr = calculate_fwhr(landmarks)
        symmetry = calculate_symmetry(landmarks)

        result = {
            "golden_ratio": g_ratio,
            "fwhr": fwhr,
            "symmetry": symmetry
        }

        output_path = os.path.join(TEMP_DIR, f"annotated_{uuid.uuid4()}.jpg")
        overlay_results(frame, landmarks, result, output_path)

        os.remove(temp_path)
        return {"scores": result, "annotated_image_url": f"/result/{os.path.basename(output_path)}"}
    except Exception as e:
        # If ANYTHING crashes, send the exact error back to the terminal!
        error_trace = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error_message": str(e), "traceback": error_trace})

@app.get("/result/{filename}")
def get_result(filename: str):
    return FileResponse(os.path.join(TEMP_DIR, filename))
