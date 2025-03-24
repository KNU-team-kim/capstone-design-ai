import os
import shutil
from collections import defaultdict

def sort_files():
    # 1. 작업해야 할 폴더 목록
    folders_to_process = [
        'tree-1',
        'tree-2',
        'tree-3',
        'tree-4'
    ]
    
    # 2. images와 labels 폴더 생성
    current_dir = os.getcwd()
    images_dir = os.path.join(current_dir, 'images')
    labels_dir = os.path.join(current_dir, 'labels')
    
    # 폴더가 없으면 생성
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    # 파일 이름별 정보를 저장할 딕셔너리
    files_by_basename = defaultdict(lambda: {'image': None, 'label': None})
    
    # 3 & 4. 모든 폴더를 검사하여 파일 목록 수집
    for folder in folders_to_process:
        if not os.path.exists(folder):
            print(f"경고: '{folder}' 폴더가 존재하지 않습니다. 건너뜁니다.")
            continue
            
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            # 디렉토리는 건너뛰기
            if os.path.isdir(file_path):
                continue
                
            # 파일 확장자 확인
            _, ext = os.path.splitext(filename)
            basename = os.path.splitext(filename)[0]  # 확장자를 제외한 파일 이름
            
            # 라벨 파일인지 이미지 파일인지 분류
            if ext.lower() in ['.txt', '.xml']:
                files_by_basename[basename]['label'] = file_path
            else:
                files_by_basename[basename]['image'] = file_path
    
    # 5. 이미지와 라벨 파일이 모두 있는 경우만 복사
    images_copied = 0
    labels_copied = 0
    
    for basename, files in files_by_basename.items():
        # 이미지와 라벨 파일이 모두 있는 경우만 처리
        if files['image'] and files['label']:
            # 이미지 파일 복사
            image_file = os.path.basename(files['image'])
            shutil.copy2(files['image'], os.path.join(images_dir, image_file))
            images_copied += 1
            
            # 라벨 파일 복사
            label_file = os.path.basename(files['label'])
            shutil.copy2(files['label'], os.path.join(labels_dir, label_file))
            labels_copied += 1
    
    # 6. 결과 출력
    print(f"작업 완료: images 폴더에 {images_copied}개 파일, labels 폴더에 {labels_copied}개 파일이 복사되었습니다.")

if __name__ == "__main__":
    sort_files()