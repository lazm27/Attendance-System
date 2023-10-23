import os
import pickle
import face_recognition
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate('C:/Users/lazee/OneDrive/Documents/facialrecognition_project/serviceaccountkey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://facial-recognition-8e923-default-rtdb.firebaseio.com/",
    'storageBucket': 'facial-recognition-8e923.appspot.com'
})

loc='C:/Users/lazee/OneDrive/Documents/facialrecognition_project/images/'
folder=os.listdir(loc)
locimg=[]
studentid=[]
for i in folder:
    locimg.append(cv2.imread(os.path.join(loc,i)))
    studentid.append(os.path.splitext(i)[0])
    #filename=os.path.join(loc,i)
    filename=f'{loc}/{i}'
    print(filename)
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)
print(studentid)

def encoder(folder):
    encodedList=[]
    for path in folder:
        img= cv2.cvtColor(path,cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        encodedList.append(encode)
    return encodedList

print("Encoding started....")
encodedlist=encoder(locimg)
encodel=[encodedlist,studentid]
print("Encoding ended")

file = open('C:/Users/lazee/OneDrive/Documents/facialrecognition_project/codes/Encoderfile.p','wb')
pickle.dump(encodel,file)
file.close()
print('File saved')

