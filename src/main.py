from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage, firestore
import fav
import datetime


#initializing Flask 
app = Flask(__name__)

#authorizing twilio client
client = Client(fav.account_sid, fav.auth_token)

#initializing firebase nonsequential database
dbapp = firestore.client()


ref = db.reference('Users/')
ref.update({'dummy data':'IDK A BETTER SOLUTION PLS HELP :SOB:'})
buck = storage.bucket(app=fav.fireapp)



ref = db.reference('Users/')
ref.update({'dummy data':'IDK A BETTER SOLUTION PLS HELP :SOB:'})

#initializing the required variables

context = []
state = 0
Izthere = 0

@app.route("/whatsapp2", methods=["POST"])
def REPLYY():

    global context
    global Izthere
 
    name = request.form.get('ProfileName')

    incoming_msg = request.form.get('Body').lower()
    phno = request.form.get('From')
    print(incoming_msg)

    context = fav.check_phno(phno,ref,name)

    curr_context = context[phno][0]['State']  #giving the state value to current context
    print(curr_context)

    match(curr_context):
          case 0: #context state is 0
               match(incoming_msg):
                    case incoming if incoming_msg in fav.initial_response:
                         context[phno][0]['State'] = 1
                         ref.update(context)

                         return fav.respond(f"Hello i'll be your assistant today what would you like to do: \n (enter 1 to use option 1 , 2 for second option and so on)\n\n 1) Register to an event \n 2) Info\n 3) exit")
                    
                    case _:
                         context[phno][0]['State'] = 0
                         ref.update(context)
                         print("res1")
                         return fav.respond(f"Invalid option \n please enter hi or hello again to start the conversation again")
               #STATE 0 END
          

          case 1: #context state is 1
               match(incoming_msg):
                    case '1':
                         i = 1
                         context[phno][0]['State'] = 2
                         ref.update(context)
                         msg = 'What event would you like to register to: \n (enter 1 to register for the first events 2 for second event and so on) \n\n'

                         for values in fav.events.values():
                              msg += f'{i}) '
                              msg += values[0]['Name']
                              msg += '\n'
                              i += 1

                         return fav.respond(msg)
                    
                    case '2':
                         context[phno][0]['State'] = 0   #checking if they registered for an event or not 
                         msg = fav.formatinfo(context)
                         return fav.respond(msg)
                    
                         
                         
                    case '3':
                         context[phno][0]['State'] = 0
                         ref.update(context)
                         
                         return fav.respond(f"Thank you for chatting with me")
                         
                         
                    case _:
                         context[phno][0]['State'] = 0   #checking if they registered for an event or not 
                         ref.update(context)
                         print("res2")
                         return fav.respond(f"Invalid option \n please enter hi or hello again to start the conversation again")
               #STATE 1 END
                    
                    
          case 2: #context state is 2
               match(incoming_msg):

                    case msg if incoming_msg in fav.events.keys():
                         print(msg)
                         context[phno][0]['State'] = 0
                         if fav.events[incoming_msg][0]['Name'] in context[phno][2]['Events']:
                              ref.update(context)
                              return fav.respond('You are already registered to this event')
                         
                         context[phno][2]['Events'].append(fav.events[msg][0]['Name']) 

                         print("what we doin")
                         url = fav.gen_QR(context)

                         if Izthere == 0:
                              print("phone no wasn't there")
                              ref.update(context)
                         else:
                              print(ref.child(phno)[0]['State'])
                              ref.update(context)

                         return fav.respond(f"thank for registering to {fav.events[msg][0]['Name']}, Here is the QR ",URL=url)
                    
                    case _:
                         print('res3')
                         context[phno][0]['State'] = 0
                         ref.update(context)

                         return fav.respond(f"Invalid option \n please enter hi or hello again to start the conversation again")
#state 2 end     
                    
@app.route("/")
def htm():
     return render_template('bgscet.html')

@app.route("/web2")
def htm2():
     return render_template('bgscetcontactus.html')
     
@app.route("/web3")
def htm3():
     return render_template('website1.html')



     

if __name__ == '__main__':  
      app.run(host='0.0.0.0',debug=1)