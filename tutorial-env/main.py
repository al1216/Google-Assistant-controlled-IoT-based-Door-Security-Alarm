import time #Import time to peform delay operations

import requests #use requests to send mail via webhooks IFTTT

from boltiot import Bolt #Import boliot to control GPIO pins through API


api_key = "2c69a837-ed50-4874-ac2f-114c9fbb3328" #Get your API key from Blot Cloud Website  

device_id  = "BOLT2910606" #Get your Bolt device ID form Bolt Cloud Website

mybolt = Bolt(api_key, device_id)


HIGH = '{"value": "1", "success": 1}' #This will be returned by bolt API if digital read is high 

LOW = '{"value": "0", "success": 1}'#This will be returned by bolt API if digital read is low


alarm = 0 #Alarm is turned off by default 


while True: #Infinite loop


    while alarm == 0: #If alarm is off

        response = mybolt.digitalRead('3') #check if it is being activated 
        print('Alarm is activated? -', response)

        if (response == HIGH):

            print("Security System is activated")

            mybolt.digitalWrite('2', 'HIGH') #Turn on LED to indicate Aalarm is activated 

            alarm = 1

        elif (response == LOW):

            print ("Waiting for Security System to be activated....")

        else:

            print ("Problem in getting value form pin 3")

        time.sleep(15) #check once in every 5 seconds to avoid exceeding API rate lmit  

    


    while alarm == 1: #If alarm is on 

        response = mybolt.digitalRead('4') #check is it is being de-activated 
        print('Alarm is de-activated? -', response)

        if (response == HIGH):

            print("Security System is De-activated")

            mybolt.digitalWrite('2', 'LOW')#Turn off LED to indicate Aalarm is De-activated 

            alarm = 0 

            time.sleep(15)

        elif (response == LOW):

            print ("Security System is currently active can be deactivated from google assistant")

        else:

            print ("Problem in getting value form pin 4")


        response = mybolt.digitalRead('0') #check if hall sensor is triggered 

        if (response == HIGH): #if magnet is not present      

            print ("Alert! Security breach Buzzer ON")

            mybolt.digitalWrite('1', 'HIGH')

            requests.get('https://maker.ifttt.com/trigger/Breach/json/with/key/ncc0s1wDOMwb63dn5u-ShK-3hCRHFs_0WVCfy5BaoTa') #webhook link to trigger mail through IFTTT
            
            requests.get('https://maker.ifttt.com/trigger/sms/json/with/key/ncc0s1wDOMwb63dn5u-ShK-3hCRHFs_0WVCfy5BaoTa') #webhook link to trigger SMS through IFTTT
            
            requests.get('https://maker.ifttt.com/trigger/SMS/json/with/key/f0zDZieIVBppq3hR0gTD7fvIWccfESiYFM2KM09dGKC')
            
            time.sleep(15)

            mybolt.digitalWrite('1', 'LOW')

            print ("Buzzer OFF")

        elif (response == LOW):

            print ("No problem, all good!")

        else:  

            print ("Problem in reading the value of button")

        time.sleep(15)