import os
import glob
import xml.etree.ElementTree as ET

def convert_annotation(xml_file, class_dict):
    """
    XML 주석 파일을 YOLO 형식으로 변환합니다.
    
    Args:
        xml_file (str): XML 파일 경로
        class_dict (dict): 클래스 이름과 ID 매핑 딕셔너리
    
    Returns:
        list: YOLO 형식의 주석 문자열 리스트
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # 이미지 크기 정보 가져오기
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    
    yolo_annotations = []
    
    # 각 객체에 대해 처리
    for obj in root.findall('object'):
        # 클래스 이름 가져오기
        class_name = obj.find('name').text
        
        # 클래스 딕셔너리에 없는 클래스는 건너뜀
        if class_name not in class_dict:
            print(f"경고: '{class_name}'은(는) 클래스 딕셔너리에 없습니다. 건너뜁니다.")
            continue
        
        class_id = class_dict[class_name]
        
        # 바운딩 박스 좌표 가져오기
        bbox = obj.find('bndbox')
        xmin = float(bbox.find('xmin').text)
        ymin = float(bbox.find('ymin').text)
        xmax = float(bbox.find('xmax').text)
        ymax = float(bbox.find('ymax').text)
        
        # YOLO 형식으로 변환
        # YOLO 형식: [class_id center_x center_y width height]
        # 여기서 모든 값은 0~1 사이로 정규화됨
        
        # 중심 좌표 계산
        center_x = (xmin + xmax) / 2.0 / width
        center_y = (ymin + ymax) / 2.0 / height
        
        # 너비와 높이 계산
        bbox_width = (xmax - xmin) / width
        bbox_height = (ymax - ymin) / height
        
        # YOLO 형식 문자열 생성
        yolo_annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}"
        yolo_annotations.append(yolo_annotation)
    
    return yolo_annotations

def process_directory():
    """
    지정된 디렉토리에서 파일들을 처리하여 필요한 경우 XML을 TXT로 변환합니다.
    """
    # 작업할 폴더 경로 
    work_directory = "./labels"
    
    # 클래스 딕셔너리
    class_dict = {
        "tree": 0,
    }
    
    # 변환된 파일 카운트
    converted_count = 0
    skipped_count = 0
    
    # 디렉토리 내 모든 파일 처리
    for file_path in glob.glob(os.path.join(work_directory, "*.*")):
        file_name, file_ext = os.path.splitext(file_path)
        
        # XML 파일인 경우만 변환
        if file_ext.lower() == '.xml':
            # 동일한 이름의 TXT 파일이 이미 있는지 확인
            txt_file_path = file_name + '.txt'
            if os.path.exists(txt_file_path):
                print(f"경고: '{txt_file_path}' 파일이 이미 존재합니다. 건너뜁니다.")
                skipped_count += 1
                continue
            
            try:
                # XML을 YOLO 형식 TXT로 변환
                yolo_annotations = convert_annotation(file_path, class_dict)
                
                # 변환 결과 저장
                with open(txt_file_path, 'w') as f:
                    for annotation in yolo_annotations:
                        f.write(annotation + '\n')
                
                print(f"변환 완료: {file_path} -> {txt_file_path}")
                converted_count += 1
                
            except Exception as e:
                print(f"오류: '{file_path}' 파일 변환 중 문제가 발생했습니다: {str(e)}")
    
    # 결과 출력
    print(f"\n처리 완료: {converted_count}개 파일 변환됨, {skipped_count}개 파일 건너뜀")

if __name__ == "__main__":
    process_directory()