import os
import re

def change_class_number(directory_path, target_class):
    # 디렉토리 내의 모든 파일 확인
    for filename in os.listdir(directory_path):
        # txt 파일만 처리
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            
            # 파일 내용 읽기
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # 수정된 내용을 저장할 리스트
            modified_lines = []
            
            # 각 줄 처리
            for line in lines:
                # 공백으로 분리된 값들
                values = line.strip().split()
                
                # 첫 번째 값이 클래스 번호
                if values and values[0].isdigit():
                    class_number = int(values[0])
                    
                    # 원하는 클래스 번호가 아니면 변경
                    if class_number != target_class:
                        values[0] = str(target_class)
                
                # 수정된 줄 다시 조합
                modified_line = ' '.join(values) + '\n'
                modified_lines.append(modified_line)
            
            # 수정된 내용을 파일에 쓰기
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)
            
            print(f"파일 {filename} 처리 완료")

# 사용 예시
if __name__ == "__main__":
    # 매개변수 설정: 폴더 경로, 변경할 원래 클래스 번호, 새로 설정할 클래스 번호
    folder_path = "labels"  # 실제 폴더 경로로 변경하세요
    target_class = 0  # 새로 설정할 클래스 번호
    
    change_class_number(folder_path, target_class)