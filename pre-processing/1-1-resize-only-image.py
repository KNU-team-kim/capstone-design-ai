import os
import cv2
import shutil

def letterbox(img, target_size=(640, 640), padding_color=(114, 114, 114)):
    h, w = img.shape[:2]
    scale = min(target_size[0] / h, target_size[1] / w)
    new_w, new_h = int(w * scale), int(h * scale)

    resized_img = cv2.resize(img, (new_w, new_h))

    # padding 계산
    pad_w = target_size[1] - new_w
    pad_h = target_size[0] - new_h
    top, bottom = pad_h // 2, pad_h - pad_h // 2
    left, right = pad_w // 2, pad_w - pad_w // 2

    # padding 추가 (Letterbox 방식)
    img_padded = cv2.copyMakeBorder(
        resized_img, top, bottom, left, right,
        cv2.BORDER_CONSTANT, value=padding_color
    )

    return img_padded

def process_images(src_folder):
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp")
    
    if not os.path.exists(src_folder):
        print(f"[ERROR] 폴더 '{src_folder}' 가 존재하지 않습니다.")
        return

    # 결과 저장 폴더
    dest_folder = f"{os.path.basename(src_folder)}_result"
    os.makedirs(dest_folder, exist_ok=True)

    img_files = [f for f in os.listdir(src_folder) if f.lower().endswith(supported_formats)]

    for img_name in img_files:
        img_path = os.path.join(src_folder, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"[WARN] '{img_name}' 파일은 이미지가 아닙니다. 건너뜁니다.")
            continue

        h, w = img.shape[:2]

        # 이미지가 이미 640×640이면 그냥 복사
        if (w, h) == (640, 640):
            shutil.copy(img_path, os.path.join(dest_folder, img_name))
            print(f"[COPY] '{img_name}' 크기 동일, 복사 완료.")
        else:
            img_processed = letterbox(img, (640, 640))
            cv2.imwrite(os.path.join(dest_folder, img_name), img_processed)
            print(f"[SAVE] '{img_name}' 변환 후 저장 완료 (원본: {w}×{h}).")

    print(f"\n✅ 이미지 처리가 완료되었습니다. 결과 폴더: '{dest_folder}'")

# 사용 예시:
if __name__ == "__main__":
    source_folder = "cups"  # << 폴더 이름을 지정하세요.
    process_images(source_folder)