import os
import cv2
import shutil
import numpy as np

def letterbox(img, target_size=(640, 640), padding_color=(114, 114, 114)):
    """
    Resize and pad image to target size using letterbox method
    Returns:
        - padded image
        - scale factor
        - padding information (top, left)
    """
    h, w = img.shape[:2]
    scale = min(target_size[0] / h, target_size[1] / w)
    new_w, new_h = int(w * scale), int(h * scale)

    resized_img = cv2.resize(img, (new_w, new_h))

    # Calculate padding
    pad_w = target_size[1] - new_w
    pad_h = target_size[0] - new_h
    top, bottom = pad_h // 2, pad_h - pad_h // 2
    left, right = pad_w // 2, pad_w - pad_w // 2

    # Add padding (Letterbox method)
    img_padded = cv2.copyMakeBorder(
        resized_img, top, bottom, left, right,
        cv2.BORDER_CONSTANT, value=padding_color
    )

    return img_padded, scale, (top, left)

def convert_yolo_coordinates(bbox, original_size, scale, padding):
    """
    Convert YOLO format bounding box coordinates to match resized image
    
    Args:
        bbox: YOLO format bounding box [class_id, center_x, center_y, width, height]
        original_size: (width, height) of original image
        scale: scale factor used in resizing
        padding: (top, left) padding values
    
    Returns:
        Updated YOLO format bounding box
    """
    class_id, center_x, center_y, width, height = bbox
    
    # Original pixel coordinates
    orig_w, orig_h = original_size
    x_center_px = center_x * orig_w
    y_center_px = center_y * orig_h
    width_px = width * orig_w
    height_px = height * orig_h
    
    # Apply scaling
    x_center_px *= scale
    y_center_px *= scale
    width_px *= scale
    height_px *= scale
    
    # Apply padding
    top, left = padding
    x_center_px += left
    y_center_px += top
    
    # Convert back to normalized coordinates (0-1) for 640x640
    center_x_new = x_center_px / 640
    center_y_new = y_center_px / 640
    width_new = width_px / 640
    height_new = height_px / 640
    
    # Clamp values to valid range (0-1)
    center_x_new = max(0, min(1, center_x_new))
    center_y_new = max(0, min(1, center_y_new))
    width_new = max(0, min(1, width_new))
    height_new = max(0, min(1, height_new))
    
    return [class_id, center_x_new, center_y_new, width_new, height_new]

def process_dataset(images_folder, labels_folder):
    """Process both images and labels for YOLO dataset"""
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp")
    
    # Check if folders exist
    if not os.path.exists(images_folder):
        print(f"[ERROR] 이미지 폴더 '{images_folder}'가 존재하지 않습니다.")
        return
    
    if not os.path.exists(labels_folder):
        print(f"[ERROR] 라벨 폴더 '{labels_folder}'가 존재하지 않습니다.")
        return
    
    # Create result folders
    images_result_folder = f"{os.path.basename(images_folder)}_result"
    labels_result_folder = f"{os.path.basename(labels_folder)}_result"
    
    os.makedirs(images_result_folder, exist_ok=True)
    os.makedirs(labels_result_folder, exist_ok=True)
    
    # Get all image files
    img_files = [f for f in os.listdir(images_folder) if f.lower().endswith(supported_formats)]
    
    for img_name in img_files:
        img_path = os.path.join(images_folder, img_name)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"[WARN] '{img_name}' 파일은 이미지가 아닙니다. 건너뜁니다.")
            continue
        
        # Get base name without extension for finding label file
        base_name = os.path.splitext(img_name)[0]
        label_file = os.path.join(labels_folder, base_name + ".txt")
        
        # Check if label file exists
        if not os.path.exists(label_file):
            print(f"[WARN] '{base_name}.txt' 라벨 파일이 없습니다. 건너뜁니다.")
            continue
        
        h, w = img.shape[:2]
        
        # If image is already 640x640, just copy both files
        if (w, h) == (640, 640):
            shutil.copy(img_path, os.path.join(images_result_folder, img_name))
            shutil.copy(label_file, os.path.join(labels_result_folder, base_name + ".txt"))
            print(f"[COPY] '{img_name}' 및 라벨 파일 크기 동일, 복사 완료.")
        else:
            # Process image with letterbox method
            img_processed, scale, padding = letterbox(img, (640, 640))
            
            # Save processed image
            cv2.imwrite(os.path.join(images_result_folder, img_name), img_processed)
            
            # Process label file
            with open(label_file, 'r') as f:
                label_lines = f.readlines()
            
            new_label_lines = []
            for line in label_lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                # Parse YOLO format: class_id center_x center_y width height
                try:
                    values = list(map(float, line.split()))
                    if len(values) != 5:
                        print(f"[WARN] 라벨 형식 오류 (항목 수 불일치): {line}")
                        continue
                        
                    # Convert coordinates for resized image
                    new_values = convert_yolo_coordinates(values, (w, h), scale, padding)
                    new_line = f"{int(new_values[0])} {new_values[1]:.6f} {new_values[2]:.6f} {new_values[3]:.6f} {new_values[4]:.6f}"
                    new_label_lines.append(new_line)
                except ValueError:
                    print(f"[WARN] 라벨 형식 오류 (숫자 변환 실패): {line}")
                    continue
            
            # Save new label file
            with open(os.path.join(labels_result_folder, base_name + ".txt"), 'w') as f:
                f.write('\n'.join(new_label_lines))
            
            print(f"[SAVE] '{img_name}' 및 라벨 변환 후 저장 완료 (원본: {w}×{h}).")
    
    print(f"\n✅ 데이터셋 처리가 완료되었습니다.")
    print(f"결과 이미지 폴더: '{images_result_folder}'")
    print(f"결과 라벨 폴더: '{labels_result_folder}'")

# 사용 예시:
if __name__ == "__main__":
    images_folder = "images"  # 이미지 폴더 경로
    labels_folder = "labels"  # 라벨 폴더 경로
    process_dataset(images_folder, labels_folder)