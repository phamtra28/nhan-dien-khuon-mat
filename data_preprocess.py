import os
import cv2
import numpy as np
import pickle
from insightface.app import FaceAnalysis

# Đường dẫn chứa ảnh của các thành viên
dataset_path = r"D:\insight\bessttt\dataset"

# Khởi tạo InsightFace để trích xuất khuôn mặt
face_app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
                          allowed_modules=['detection', 'recognition'])  
face_app.prepare(ctx_id=0, det_size=(640, 640))

# Dictionary lưu embeddings và thông tin sinh viên
face_db = {}

# Duyệt qua từng ảnh trong dataset
for img_name in os.listdir(dataset_path): # lấy tất cả các danh sách ảnh trong thư mụcmục
    img_path = os.path.join(dataset_path, img_name) # kết hợp đường dẫn với thư mụcmục

    # Đọc ảnh
    img = cv2.imread(img_path)
    if img is None:
        print(f"Lỗi đọc ảnh {img_name}")
        continue

    # Phát hiện khuôn mặt
    faces = face_app.get(img) #nhận diện khuôn mặt trong ảnh
    if len(faces) == 0:
        print(f"Không tìm thấy khuôn mặt trong ảnh {img_name}")
        continue

    # Lấy đặc trưng khuôn mặt (embedding)
    face_embedding = faces[0].embedding #Lấy embedding của khuôn mặt đầu tiên phát hiện được.

    # Tách thông tin từ tên file (MãSV, Họ tên, Lớp)
    try:
        student_id, name, class_name = img_name[:-4].split("_") #tách chuỗi theo ký tự _
    except ValueError:
        print(f"Lỗi: Tên file '{img_name}' không đúng định dạng!")
        continue

    # Lưu vào dictionary
    face_db[student_id] = {
        "embedding": face_embedding,
        "name": name,
        "class": class_name
    }

# Lưu embeddings vào file
with open("face_db.pkl", "wb") as f:
    pickle.dump(face_db, f) # lưu vào tệp dưới dạng nhị phânphân

print("✅ Dataset đã được xử lý và lưu vào 'face_db.pkl'")
