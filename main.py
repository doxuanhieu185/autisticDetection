from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
classifier =load_model('./Emotion_Detection.h5')
videopath = './abnormal.mp4'
class_labels = ['tuc gian','vui ve','binh thuong','buon','bat ngo']

cap = cv2.VideoCapture(1)
status = []


while True:
    # Lấy một khung hình video
    ret, frame = cap.read()
    if ret is False or frame is None:  # Kiểm tra xem frame có giá trị hay không
        break
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

# ve hinh chu nhat xung quanh khuon mat
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

# neu vung trong tam co gia tri thi convert sang mang
        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

# nhan dien cam xuc
            preds = classifier.predict(roi)[0]
            label=class_labels[preds.argmax()]
            status.append(preds.argmax())
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        else:
            cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        print("\n\n")
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cnt_status = len(set(status))
if cnt_status >=3:
    print("có dấu hiệu tự kỷ !!")
else:
    print("Bình thường")
cap.release()
cv2.destroyAllWindows()






