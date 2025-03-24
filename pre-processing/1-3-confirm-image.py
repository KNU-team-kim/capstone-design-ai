"""
1-2 코드사용해서 변환했을 때, 확인용으로 사용.
"""

import os
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

def visualize_bounding_boxes(images_folder, labels_folder, output_folder, num_samples=10):
    """
    변환된 이미지와 라벨을 불러와 바운딩 박스를 시각화하는 함수
    
    Args:
        images_folder: 변환된 이미지가 있는 폴더 경로
        labels_folder: 변환된 라벨이 있는 폴더 경로
        output_folder: 시각화 결과를 저장할 폴더 경로
        num_samples: 시각화할 이미지 샘플 수
    """
    # 결과 폴더 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # 지원하는 이미지 형식
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp")
    
    # 이미지 파일 목록 가져오기
    img_files = [f for f in os.listdir(images_folder) if f.lower().endswith(supported_formats)]
    
    # 샘플 수 제한
    if len(img_files) > num_samples:
        # 랜덤 샘플링
        img_files = random.sample(img_files, num_samples)
        
    print(f"총 {len(img_files)}개 이미지에 대한 바운딩 박스를 시각화합니다.")
    
    # 클래스별 색상 랜덤 생성 (최대 20개 클래스 가정)
    colors = {}
    
    # 각 이미지에 대해 바운딩 박스 시각화
    for img_name in img_files:
        # 이미지 로드
        img_path = os.path.join(images_folder, img_name)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"[WARN] '{img_name}' 이미지를 읽을 수 없습니다. 건너뜁니다.")
            continue
            
        # RGB로 변환 (OpenCV는 BGR로 읽음)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 이미지 크기 가져오기
        height, width = img.shape[:2]
        
        # 라벨 파일 경로
        base_name = os.path.splitext(img_name)[0]
        label_path = os.path.join(labels_folder, base_name + ".txt")
        
        # 라벨 파일이 존재하는지 확인
        if not os.path.exists(label_path):
            print(f"[WARN] '{base_name}.txt' 라벨 파일이 없습니다. 건너뜁니다.")
            continue
            
        # 라벨 파일 읽기
        with open(label_path, 'r') as f:
            lines = f.readlines()
            
        # 그림 생성
        plt.figure(figsize=(10, 10))
        plt.imshow(img_rgb)
        plt.title(f"Image: {img_name}")
        
        # 각 바운딩 박스 그리기
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # YOLO 형식: 클래스 ID, 중심 x, 중심 y, 너비, 높이
            try:
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.split())
                class_id = int(class_id)
                
                # 클래스별 색상 생성 (처음 보는 클래스면 새 색상 생성)
                if class_id not in colors:
                    colors[class_id] = (random.random(), random.random(), random.random())
                
                # 바운딩 박스 좌표 계산 (YOLO 형식 -> 픽셀 좌표)
                # (중심 x, 중심 y, 너비, 높이) -> (왼쪽 위 x, 왼쪽 위 y, 오른쪽 아래 x, 오른쪽 아래 y)
                x_center, y_center = int(x_center * width), int(y_center * height)
                bbox_width, bbox_height = int(bbox_width * width), int(bbox_height * height)
                
                x1 = int(x_center - bbox_width / 2)
                y1 = int(y_center - bbox_height / 2)
                x2 = int(x_center + bbox_width / 2)
                y2 = int(y_center + bbox_height / 2)
                
                # 바운딩 박스 그리기
                rect = plt.Rectangle((x1, y1), bbox_width, bbox_height, 
                                     linewidth=2, edgecolor=colors[class_id], facecolor='none')
                plt.gca().add_patch(rect)
                
                # 클래스 ID 표시
                plt.text(x1, y1-5, f"Class {class_id}", 
                         color='white', bbox=dict(facecolor=colors[class_id], alpha=0.8))
                
            except ValueError:
                print(f"[WARN] '{base_name}.txt'의 라벨 형식이 잘못되었습니다: {line}")
                continue
                
        # 축 숨기기
        plt.axis('off')
        
        # 그림 저장
        output_path = os.path.join(output_folder, f"bbox_{base_name}.png")
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        
        print(f"[SAVE] '{img_name}' 바운딩 박스 시각화 완료: {output_path}")
        
    print(f"\n✅ 바운딩 박스 시각화가 완료되었습니다. 결과 폴더: '{output_folder}'")
    
    return colors  # 클래스별 색상 정보 반환

# 사용 예시
if __name__ == "__main__":
    # 폴더 경로 설정
    images_result_folder = "images_result"  # 변환된 이미지 폴더
    labels_result_folder = "labels_result"  # 변환된 라벨 폴더
    visualization_folder = "bbox_visualization"  # 시각화 결과 저장 폴더
    
    # 바운딩 박스 시각화 실행 (상위 10개 샘플)
    class_colors = visualize_bounding_boxes(
        images_result_folder, 
        labels_result_folder, 
        visualization_folder, 
        num_samples=10
    )
    
    # 사용된 클래스 및 색상 정보 출력
    print("\n사용된 클래스 ID와 색상 정보:")
    for class_id, color in class_colors.items():
        print(f"클래스 ID {class_id}: RGB{color}")