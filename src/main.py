import os
from ingestion import prepare_frame
from mesh import get_landmarks
import math_engine as math_eng
import visualize as vis

def run_pipeline():
    print("========================================")
    print("  APHRODITE ENGINE - COMPLETE RUN  ")
    print("========================================")
    
    test_image_path = "assets/test.jpg"
    img_rgb = prepare_frame(test_image_path)
    
    if img_rgb is None: return
        
    print("1. Extracting Facial Landmarks...")
    landmarks = get_landmarks(img_rgb)
    if not landmarks: return
        
    print("2. Running Math Engine...")
    g_ratio, g_variance = math_eng.calculate_golden_ratio(landmarks)
    fwhr = math_eng.calculate_fwhr(landmarks)
    symmetry = math_eng.calculate_symmetry(landmarks)
    
    metrics = {
        "golden_ratio": g_ratio,
        "fwhr": fwhr,
        "symmetry": symmetry
    }
    
    print("3. Generating Visualization...")
    output_path = vis.overlay_results(img_rgb, landmarks, metrics)
    print(f"[SUCCESS] Render saved to: {output_path}")
    
    print("\n====== FINAL ANALYSIS REPORT ======")
    print(f"* Golden Ratio: {g_ratio:.3f} (Ideal is 1.618)")
    print(f"  -> Variance from ideal: {g_variance:.3f}")
    print(f"* fWHR (Width/Height): {fwhr:.3f}")
    print(f"* Bilateral Symmetry: {symmetry:.1f}%")
    print("========================================")

if __name__ == "__main__":
    run_pipeline()
