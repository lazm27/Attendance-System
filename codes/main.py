import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate('C:/Users/lazee/OneDrive/Documents/facialrecognition_project/serviceaccountkey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://facial-recognition-8e923-default-rtdb.firebaseio.com/",
    'storageBucket': 'facial-recognition-8e923.appspot.com'
})
bucket=storage.bucket()

cap=cv2.VideoCapture(0)
imgbackground=cv2.imread('C:/Users/lazee/OneDrive/Documents/facialrecognition_project/resources/background.png')
cap.set(3,640)
cap.set(4,480)
I=[]
loc='C:/Users/lazee/OneDrive/Documents/facialrecognition_project/resources/Modes/'
folder=os.listdir(loc)
locmode=[]
for i in folder:
    locmode.append(cv2.imread(os.path.join(loc,i)))
    
file= open('C:/Users/lazee/OneDrive/Documents/facialrecognition_project/codes/Encoderfile.p','rb')
Encoding=pickle.load(file)
file.close()
encodinglist, studentid=Encoding
print(studentid)


modType=0
counter=0
id=0
imgstud=[]

while True:
    succ, frame= cap.read()
    imgS=cv2.resize(frame,(0,0),None,0.25,0.25)
    imgS= cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    currentimage=face_recognition.face_locations(imgS)
    encodeimgs=face_recognition.face_encodings(imgS,currentimage)
    imgbackground[162:162+480,55:55+640]=frame
    imgbackground[44:44+633,808:808+414]=locmode[modType]
    if currentimage:
        for fl,fe in zip(currentimage,encodeimgs):
            facecomp=face_recognition.compare_faces(encodinglist,fe)
            facedis=face_recognition.face_distance(encodinglist,fe)
            #print(facecomp)
            #print(facedis)
            minindex=np.argmin(facedis)
            if facecomp[minindex]:
                #print("Known face detected")
                #print(studentid[minindex])
                y1,x2,y2,x1=fl
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox=55+x1,162+y1,x2-x1,y2-y1
                brd=cvzone.cornerRect(imgbackground,bbox,rt=0)
                if counter==0:
                    counter=1
                    id=studentid[minindex]
                    modType=1
                    #imgbackground[44:44+633,808:808+414]=locmode[modType]
                
            if counter!=0:
                if counter==1:
                    studentinfo=db.reference(f'Students/{id}').get()
                    blob=bucket.get_blob(f'C:/Users/lazee/OneDrive/Documents/facialrecognition_project/images/{id}.jpg')
                    array=np.frombuffer(blob.download_as_string(),np.uint8)
                    imgstud=cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    
                    
                    datetimeobj=datetime.strptime(studentinfo['last_attendance_time'],'%Y-%m-%d %H:%M:%S')
                    secondselapsed=(datetime.now()-datetimeobj).total_seconds()
                    
                    if secondselapsed>30:
                        ref=db.reference(f'Students/{id}')
                        studentinfo['total_attendance']+=1
                        ref.child('total_attendance').set(studentinfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        modType=3
                        counter=0
                        imgbackground[44:44+633,808:808+414]=locmode[modType]

                if modType!=3:
                
                    if 10<counter<20:
                        modType=2
                    
                    imgbackground[44:44+633,808:808+414]=locmode[modType]
            
                        
                    if counter<=10:
                        
                        cv2.putText(imgbackground, str(studentinfo['total_attendance']), (861, 125),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(studentinfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(id), (1006, 493),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(studentinfo['standing']), (910, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgbackground, str(studentinfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgbackground, str(studentinfo['Starting_year']), (1125, 625),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        (w,h),_=cv2.getTextSize(studentinfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                        offset=(414-w)//2
                        cv2.putText(imgbackground, str(studentinfo['name']), (808+offset, 445),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (50,50, 50), 1)
                        imgstud=cv2.resize(imgstud,(216,216))
                        imgbackground[175:175 + 216, 909:909 + 216]=imgstud
                    counter+=1
                        
                    if counter>20:
                        modType=0
                        imgstud=[]
                        counter=0
                        studentinfo=[]
                        imgbackground[44:44+633,808:808+414]=locmode[modType]
                        
    else:
        modType=0
        counter=0
        imgbackground[44:44+633,808:808+414]=locmode[modType]
            
        
            
   
    #cv2.imshow('VideoCapture',frame)
    cv2.imshow('Background',imgbackground)
    cv2.waitKey(1)
    if cv2.waitKey(1)==ord('q'):
        cv2.destroyAllWindows()
        break

