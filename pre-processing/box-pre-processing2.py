import os
import glob

def remove_empty_files_and_matching_images():
    """
    labels 폴더 내 빈 텍스트 파일과 images 폴더 내 매칭되는 이미지 파일을 제거합니다.
    """
    # 폴더 경로 설정
    labels_dir = "labels"
    images_dir = "images"
    
    # 경로가 존재하는지 확인
    if not os.path.exists(labels_dir) or not os.path.exists(images_dir):
        print(f"오류: '{labels_dir}' 또는 '{images_dir}' 폴더가 존재하지 않습니다.")
        return
    
    # 제거된 파일 카운트
    removed_txt_count = 0
    removed_img_count = 0
    
    # labels 폴더 내의 모든 txt 파일 처리
    for txt_path in glob.glob(os.path.join(labels_dir, "*.txt")):
        # 파일 크기 확인
        if os.path.getsize(txt_path) == 0:
            base_name = os.path.basename(txt_path)
            name_without_ext = os.path.splitext(base_name)[0]
            
            # 매칭되는 이미지 파일 찾기
            matching_images = []
            for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff']:
                img_path = os.path.join(images_dir, name_without_ext + ext)
                if os.path.exists(img_path):
                    matching_images.append(img_path)
            
            # 빈 txt 파일 제거
            try:
                os.remove(txt_path)
                removed_txt_count += 1
                print(f"제거됨: {txt_path}")
                
                # 매칭되는 이미지 파일 제거
                for img_path in matching_images:
                    try:
                        os.remove(img_path)
                        removed_img_count += 1
                        print(f"제거됨: {img_path}")
                    except Exception as e:
                        print(f"오류: '{img_path}' 파일 제거 중 문제가 발생했습니다: {str(e)}")
                
            except Exception as e:
                print(f"오류: '{txt_path}' 파일 제거 중 문제가 발생했습니다: {str(e)}")
    
    # 결과 출력
    print(f"\n처리 완료: {removed_txt_count}개의 빈 텍스트 파일과 {removed_img_count}개의 매칭 이미지 파일이 제거되었습니다.")

if __name__ == "__main__":
    # 확인 메시지 표시
    print("이 스크립트는 labels 폴더 내 빈 텍스트 파일과 images 폴더 내 매칭되는 이미지 파일을 제거합니다.")
    confirm = input("계속하시겠습니까? (y/n): ")
    
    if confirm.lower() == 'y':
        remove_empty_files_and_matching_images()
    else:
        print("작업이 취소되었습니다.")