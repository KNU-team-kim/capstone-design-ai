import os
import shutil

def clean_box_data(labels_dir='labels', images_dir='images'):
    """
    box-labels 디렉토리 내의 txt 파일들을 검사하여 조건에 맞지 않는 파일과
    해당 파일과 동일한 이름의 이미지 파일을 삭제합니다.
    
    조건: 파일 내 각 줄의 첫 번째 숫자가 0, 1, 2, 3, 7 중 하나여야 함
    
    Args:
        labels_dir (str): 라벨 파일이 있는 디렉토리 경로
        images_dir (str): 이미지 파일이 있는 디렉토리 경로
    
    Returns:
        tuple: 삭제된 라벨 파일 수, 삭제된 이미지 파일 수
    """
    # 유효한 클래스 ID 목록
    valid_class_ids = {'0', '1', '2', '3', '7'}
    
    # 삭제된 파일 카운터
    deleted_label_count = 0
    deleted_image_count = 0
    
    # box-labels 디렉토리 내의 모든 txt 파일 검사
    for filename in os.listdir(labels_dir):
        if not filename.endswith('.txt'):
            continue
            
        label_path = os.path.join(labels_dir, filename)
        
        # 파일 삭제 여부를 결정하는 플래그
        should_delete = False
        
        try:
            with open(label_path, 'r') as f:
                for line in f:
                    # 각 줄을 공백으로 분리
                    parts = line.strip().split()
                    
                    # 줄이 비어있지 않고 첫 번째 값이 유효한 클래스 ID가 아닌 경우
                    if parts and parts[0] not in valid_class_ids:
                        should_delete = True
                        break
        except Exception as e:
            print(f"파일 {filename} 처리 중 오류 발생: {e}")
            continue
            
        # 조건에 맞지 않는 경우 파일 삭제
        if should_delete:
            # 매칭되는 이미지 파일 이름 생성 (확장자가 다를 수 있음)
            image_basename = os.path.splitext(filename)[0]
            
            # 라벨 파일 삭제
            try:
                os.remove(label_path)
                deleted_label_count += 1
                print(f"라벨 파일 삭제됨: {filename}")
            except Exception as e:
                print(f"라벨 파일 {filename} 삭제 중 오류 발생: {e}")
            
            # 매칭되는 이미지 파일 검색 및 삭제
            for img_file in os.listdir(images_dir):
                img_basename = os.path.splitext(img_file)[0]
                if img_basename == image_basename:
                    try:
                        img_path = os.path.join(images_dir, img_file)
                        os.remove(img_path)
                        deleted_image_count += 1
                        print(f"이미지 파일 삭제됨: {img_file}")
                    except Exception as e:
                        print(f"이미지 파일 {img_file} 삭제 중 오류 발생: {e}")
    
    return deleted_label_count, deleted_image_count

if __name__ == "__main__":
    # 디렉토리가 존재하는지 확인
    if not os.path.exists('labels'):
        print("box-labels 디렉토리가 존재하지 않습니다.")
        exit(1)
        
    if not os.path.exists('images'):
        print("box-images 디렉토리가 존재하지 않습니다.")
        exit(1)
    
    # 함수 실행
    deleted_labels, deleted_images = clean_box_data()
    
    # 결과 출력
    print(f"\n작업 완료:")
    print(f"삭제된 라벨 파일 수: {deleted_labels}")
    print(f"삭제된 이미지 파일 수: {deleted_images}")