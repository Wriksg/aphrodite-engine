import cv2
import os

def overlay_results(img_rgb, landmarks, metrics, output_path="output/annotated_result.jpg"):
    """Draws points, lines, and text on the image and saves it."""
    # Convert RGB back to BGR so OpenCV saves the colors correctly
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Define colors in BGR format
    COLOR_POINT = (0, 255, 255)   # Yellow
    COLOR_LINE_GR = (255, 0, 255) # Magenta (Golden Ratio)
    COLOR_LINE_FW = (0, 165, 255) # Orange (fWHR)
    COLOR_LINE_SYM = (255, 255, 0) # Cyan (Symmetry)
    COLOR_TEXT = (0, 255, 0)      # Green

    # 1. Draw main measurement lines
    cv2.line(img_bgr, landmarks["hairline"], landmarks["chin"], COLOR_LINE_GR, 2)
    cv2.line(img_bgr, landmarks["left_cheek"], landmarks["right_cheek"], COLOR_LINE_GR, 2)
    cv2.line(img_bgr, landmarks["brow_mid"], landmarks["upper_lip"], COLOR_LINE_FW, 2)

    # 2. Draw symmetry lines (from points to the nose)
    for pt in ["left_eye", "right_eye", "left_mouth", "right_mouth"]:
        cv2.line(img_bgr, landmarks[pt], landmarks["nose_tip"], COLOR_LINE_SYM, 1)

    # 3. Draw the anchor points (dots)
    for name, coords in landmarks.items():
        cv2.circle(img_bgr, coords, 5, COLOR_POINT, -1)

    # 4. Add the HUD Text Box
    font = cv2.FONT_HERSHEY_SIMPLEX
    texts = [
        f"Golden Ratio: {metrics['golden_ratio']:.3f}",
        f"fWHR: {metrics['fwhr']:.3f}",
        f"Symmetry: {metrics['symmetry']:.1f}%"
    ]
    
    y_offset = 30
    for text in texts:
        # Draw a black shadow for readability
        cv2.putText(img_bgr, text, (22, y_offset + 2), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        # Draw the actual text
        cv2.putText(img_bgr, text, (20, y_offset), font, 0.7, COLOR_TEXT, 2, cv2.LINE_AA)
        y_offset += 30

    # 5. Save the file
    os.makedirs("output", exist_ok=True)
    cv2.imwrite(output_path, img_bgr)
    return output_path
