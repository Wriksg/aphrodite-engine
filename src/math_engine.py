import math

def euclidean_distance(p1, p2):
    """Calculates the straight-line distance between two (x, y) points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def calculate_golden_ratio(landmarks):
    """Module A: Compares Face Length / Face Width to Phi (1.618)."""
    length = euclidean_distance(landmarks["hairline"], landmarks["chin"])
    width = euclidean_distance(landmarks["left_cheek"], landmarks["right_cheek"])
    
    if width == 0: return 0.0, 0.0
        
    ratio = length / width
    ideal_phi = 1.618
    variance = abs(ratio - ideal_phi)
    
    return ratio, variance

def calculate_fwhr(landmarks):
    """Module B: Facial Width-to-Height Ratio."""
    width = euclidean_distance(landmarks["left_cheek"], landmarks["right_cheek"])
    height = euclidean_distance(landmarks["brow_mid"], landmarks["upper_lip"])
    
    if height == 0: return 0.0
        
    return width / height

def calculate_symmetry(landmarks):
    """Module C: Bilateral Symmetry. 100% is perfectly symmetrical."""
    center = landmarks["nose_tip"]
    
    pairs = [
        ("left_eye", "right_eye"),
        ("left_cheek", "right_cheek"),
        ("left_mouth", "right_mouth")
    ]
    
    total_score = 0
    
    for left, right in pairs:
        dist_left = euclidean_distance(landmarks[left], center)
        dist_right = euclidean_distance(landmarks[right], center)
        
        # Calculate percentage difference (100% = identical distances)
        max_dist = max(dist_left, dist_right)
        if max_dist == 0:
            pair_score = 100.0
        else:
            diff = abs(dist_left - dist_right)
            pair_score = 100.0 - ((diff / max_dist) * 100.0)
            
        total_score += pair_score
        
    # Return average symmetry across all pairs
    return total_score / len(pairs)
