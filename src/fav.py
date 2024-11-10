from twilio.twiml.messaging_response import MessagingResponse
import ourQR
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage, firestore
import datetime

cred = credentials.Certificate("{YOUR FIREBASE CREDENTIALS}")
fireapp = firebase_admin.initialize_app(cred, {'databaseURL':'[FIREBASE  REALTIME DATABASE LINK]' , 
                                     'storageBucket':'FIREBASE STORAGE URL'})

dbapp = firestore.client()


ref = db.reference('Users/')
ref.update({'dummy data':'IDK A BETTER SOLUTION PLS HELP :SOB:'})
buck = storage.bucket(app=fireapp)

#VARIABLES
#event Details
events = { '1':[{'Name':'Dancing'},{'Desc':'NONE'}],
           '2':[{'Name':'Singing'},{'Desc':'NONE'}], 
           '3':[{'Name':'Treasure Hunt'},{'Desc':'NONE'}],
           '4':[{'Name':'Fashion show'},{'Desc':'NONE'}], 
           '5':[{'Name':'Hackathon'},{'Desc':'NONE'}], 
           '6':[{'Name':'Debugging'},{'Desc':'NONE'}]}     

initial_response = ['hi','hello','hey','ola','hii','konichiwa','annoyeong']

account_sid = '[YOUR TWILIO ACCOUNT SID]' #twilio account SID
auth_token = '[YOUR TWILIO ACCOUNT AUTH TOKEN]' #Twilio Auth token


#FUNCTIONS 

#func to check if phone no exists in database or not
def check_phno(phone_no,ref,name):
      if phone_no in ref.get().keys():
            print("phone number already exists")
            contextref = ref.get()[phone_no]
            if (len(contextref) == 2):
                 contextref.append({'Events':[]})

            tempcon = {phone_no:contextref}
                 
            return tempcon
      else:
           print("phone number is not there")
           state = 0
           tempcon = {phone_no:[{'State':state},{"Name":name},{'Events':[]}]}
           ref.update(tempcon)
           return tempcon
      
#function to send a whatsapp message
def respond(message,URL=''):
     response = MessagingResponse()
     response.message().body(message)
     response.message().media(URL)
     print(response)
     return str(response)

#function to store image in db
def storeimg(filepath,name):
      print(filepath)
      filename = f"{filepath}"
      blob = buck.blob(f'{name}.jpg')
      blob.upload_from_filename(filename=filename)
      blob.make_public()

def get_img(Filename):
     
     blob = buck.get_blob(f'{Filename}.jpg')
     url =  blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
      )
     print("URL:",url)
     return url

#function to generate qr and store in server
def gen_QR(context):
     Filepath,Filename = ourQR.generate_qr_code(context)

     storeimg(Filepath,Filename)

     print('did it work')
     url = get_img(Filename)
  
     return url


#function to format context data
def formatinfo(context):
     inf =""
     for temp in context.keys():
          temp1 = temp
          useless,phno = temp.split('+')

     for event in context[temp1][2]['Events']:
          inf += f"{event}    "
          if(len(context[temp1][2]['Events']) != 1):
               inf += f", "
 
     formated_str = f"Phone number: {phno} \n Name: {context[temp1][1]['Name']} \n Events : {inf}"

     return formated_str

