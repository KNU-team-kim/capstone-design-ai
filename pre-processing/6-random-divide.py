import os
import random
import shutil
from pathlib import Path
import sys

def split_data(images_dir='images', labels_dir='labels', split_ratio=(0.7, 0.2, 0.1)):
    # 비율의 합이 1인지 확인
    assert abs(sum(split_ratio) - 1.0) < 0.001, "분할 비율의 합은 1이어야 합니다."
    
    # 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    
    # 랜덤하게 섞기
    random.shuffle(image_files)
    
    # 분할 인덱스 계산
    train_end = int(len(image_files) * split_ratio[0])
    valid_end = train_end + int(len(image_files) * split_ratio[1])
    
    # 세트 분할
    train_files = image_files[:train_end]
    valid_files = image_files[train_end:valid_end]
    test_files = image_files[valid_end:]
    
    # 각 세트별 데이터 복사 함수
    def copy_files(files, subset):
        # 이미지 폴더 생성
        img_target_dir = os.path.join(images_dir, subset)
        Path(img_target_dir).mkdir(parents=True, exist_ok=True)
        
        # 레이블 폴더 생성
        label_target_dir = os.path.join(labels_dir, subset)
        Path(label_target_dir).mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # 이미지 파일 이름에서 확장자 제거
            file_base = os.path.splitext(file)[0]
            
            # 이미지 파일 복사
            img_src = os.path.join(images_dir, file)
            img_dst = os.path.join(img_target_dir, file)
            shutil.copy2(img_src, img_dst)
            
            # 레이블 파일 복사 (txt 확장자로 가정)
            label_file = file_base + '.txt'
            label_src = os.path.join(labels_dir, label_file)
            label_dst = os.path.join(label_target_dir, label_file)
            
            # 레이블 파일이 존재하는지 확인
            if os.path.exists(label_src):
                shutil.copy2(label_src, label_dst)
            else:
                print(f"경고: {label_src} 레이블 파일을 찾을 수 없습니다.")
                sys.exit(1)
    
    # 각 세트별로 파일 복사
    copy_files(train_files, 'train')
    copy_files(valid_files, 'valid')
    copy_files(test_files, 'test')
    
    # 결과 출력
    print(f"데이터 분할 완료:")
    print(f"  - 학습 세트: {len(train_files)} 파일")
    print(f"  - 검증 세트: {len(valid_files)} 파일")
    print(f"  - 테스트 세트: {len(test_files)} 파일")

if __name__ == "__main__":
    # 기본 디렉토리 구조가 존재하는지 확인
    if not os.path.exists('images'):
        print("오류: 'images' 폴더가 존재하지 않습니다.")
        exit(1)
    
    if not os.path.exists('labels'):
        print("오류: 'labels' 폴더가 존재하지 않습니다.")
        exit(1)
    
    # 7:2:1 비율로 데이터 분할
    split_data(split_ratio=(0.7, 0.2, 0.1))