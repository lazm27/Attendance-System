import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv
load_dotenv()
cred = credentials.Certificate('serviceaccountkey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': os.getenv("DATABASEURL"),
})

ref=db.reference('Students')

data={
    '875432':
        {
            'name':"Lazeen Manasia",
            'year':4,
            'major':'Robotics',
            'Starting_year':2018,
            'standing':'G',
            'total_attendance':6,
            'last_attendance_time':'2023-05-06 00:54:34'       
        
        },
    '234567':
        {
            'name':"Kismat Manasia",
            'year':4,
            'major':'Robotics',
            'Starting_year':2018,
            'standing':'G',
            'total_attendance':6,
            'last_attendance_time':'2023-05-06 00:54:34'       
        },
    '961234':
        {
            'name':"Adiv Manasia",
            'year':1,
            'major':'Advanced Math',
            'Starting_year':2018,
            'standing':'G',
            'total_attendance':6,
            'last_attendance_time':'2023-05-06 00:54:34'       
        }
}

for key,value in data.items():
    ref.child(key).set(value)