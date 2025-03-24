import os
import shutil
import argparse
from pathlib import Path


def split_files_into_folders(source_folder, dest_folder_prefix, batch_size):
    """
    특정 폴더에 있는 이미지 파일들을 지정된 단위로 나누어 새로운 폴더에 저장합니다.
    
    Args:
        source_folder (str): 원본 이미지 파일이 있는 폴더 경로
        dest_folder_prefix (str): 생성될 목적지 폴더의 접두사 
        batch_size (int): 각 폴더에 저장할 파일 단위 수
    """
    # 소스 폴더가 존재하는지 확인
    if not os.path.exists(source_folder):
        print(f"오류: 소스 폴더 '{source_folder}'가 존재하지 않습니다.")
        return
    
    # 이미지 파일 확장자 (필요에 따라 추가 가능)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # 소스 폴더에서 이미지 파일만 필터링하고 이름순으로 정렬
    image_files = []
    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    # 파일 이름순으로 정렬
    image_files.sort()
    
    total_files = len(image_files)
    
    if total_files == 0:
        print(f"'{source_folder}' 폴더에 이미지 파일이 없습니다.")
        return
    
    # 필요한 폴더 수 계산
    num_folders = (total_files + batch_size - 1) // batch_size  # 올림 나누기
    
    print(f"총 {total_files}개의 이미지 파일을 {batch_size}개 단위로 {num_folders}개의 폴더로 나눕니다.")
    
    # 각 폴더에 파일 복사
    for folder_index in range(num_folders):
        # 새 폴더 생성
        new_folder_name = f"{dest_folder_prefix}-{folder_index + 1}"
        new_folder_path = os.path.join(os.path.dirname(source_folder), new_folder_name)
        
        # 폴더가 이미 존재하는 경우 처리
        if os.path.exists(new_folder_path):
            print(f"경고: '{new_folder_name}' 폴더가 이미 존재합니다. 기존 파일을 덮어쓸 수 있습니다.")
        else:
            os.makedirs(new_folder_path)
            print(f"'{new_folder_name}' 폴더를 생성했습니다.")
        
        # 현재 배치의 시작 및 끝 인덱스 계산
        start_idx = folder_index * batch_size
        end_idx = min((folder_index + 1) * batch_size, total_files)
        
        # 현재 배치의 파일 복사
        for i in range(start_idx, end_idx):
            src_file = os.path.join(source_folder, image_files[i])
            dst_file = os.path.join(new_folder_path, image_files[i])
            shutil.copy2(src_file, dst_file)
        
        print(f"'{new_folder_name}' 폴더에 {end_idx - start_idx}개의 파일을 복사했습니다.")


if __name__ == "__main__":
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description='이미지 파일을 지정된 단위로 나누어 폴더에 저장합니다.')
    parser.add_argument('source_folder', help='원본 이미지 파일이 있는 폴더 경로')
    parser.add_argument('dest_folder_prefix', help='목적지 폴더의 접두사 (예: "특정폴더")')
    parser.add_argument('batch_size', type=int, help='각 폴더에 저장할 파일 단위 수')
    
    args = parser.parse_args()
    
    split_files_into_folders(args.source_folder, args.dest_folder_prefix, args.batch_size)