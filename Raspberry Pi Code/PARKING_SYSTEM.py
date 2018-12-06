import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servoPIN=13  #servo pin 1
GPIO.setup(servoPIN,GPIO.OUT) # servo 1
p = GPIO.PWM(servoPIN, 50) # GPIO 13 for PWM with 50Hz
p.start(2.5) # Initialization
p.ChangeDutyCycle(0)
servoPin2=26  # servo pin 2
GPIO.setup(servoPin2,GPIO.OUT)  #servo 2
p1= GPIO.PWM(servoPin2,50)    # GPIO 26 pWM 50Hz
p1.start(2.5)
p1.ChangeDutyCycle(0)

GPIO.setup(18,GPIO.OUT)  #led1
GPIO.setup(27,GPIO.OUT)  #led2
GPIO.setup(17,GPIO.IN)  # ir1
GPIO.setup(22,GPIO.IN)  #ir2 
from firebase import firebase
firebase = firebase.FirebaseApplication('https://parkingsystem-4f32e.firebaseio.com/',None)
GPIO.output(18,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
arrv=0
arrv2=0
exitup=0
exitup2=0
while True:
    #pygame.display.flip()
    #screen.blit(t2,(230,15))
    #pygame.draw.lines(screen,black,False,[(320,50),(320,300)],2)
    result=firebase.get('/User',None)
    #print result
    ir1=GPIO.input(17)
    ir2=GPIO.input(22)
    if result[1]["slot1"]["status"]=="booked" :
        GPIO.output(18,GPIO.LOW)
        text="Booked Slot 1"
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50))    
    else:
        GPIO.output(18,GPIO.HIGH)
        text="Free Slot 1               "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50)) 
    if result[1]["slot2"]["status"]=="booked" :
        GPIO.output(27,GPIO.LOW)
        text="Booked Slot 2"
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
    else:
        GPIO.output(27,GPIO.HIGH)
        text="Free Slot 2           "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
        
    if result[1]["slot1"]["arrived"]=="1" and arrv==0:
        print("servo up")
        p.ChangeDutyCycle(7.5)
        time.sleep(1)
        arrv=1
        text="Arrvied at Gate 1"
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50))
        #servo up
        #p.ChangeDutyCycle(5)
    if result[1]["slot1"]["arrived"]=="1" and ir1==1:
        print("servo down")
        p.ChangeDutyCycle(2.5)
        time.sleep(1)
        text="Parked Slot 1           "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50))
        #screen.blit(asurf,(50,70))
        #servo down
        #p.ChnageDutyCycle(7.5)
        firebase.put('/User/1/slot1','arrived',str(2))
        #result[1]["slot1"]["arrived"]=2
    if result[1]["slot1"]["exit"]=="1" and exitup==0 and result[1]["slot1"]["arrived"]=="2":
        print("servo up exit")#servo up
        exitup=1
        p.ChangeDutyCycle(7.5)
        time.sleep(1)
    if ir1==0 and result[1]["slot1"]["exit"]=="1" and result[1]["slot1"]["arrived"]=="2":
        print("servo down exit")
        p.ChangeDutyCycle(2.5) #servo down
        time.sleep(1)
        #result[status,arrived,exit]=0
        arrv=0
        exitup=0
        firebase.put('/User/1/slot1','status',"not booked")
        firebase.put('/User/1/slot1','arrived',str(0))
        firebase.put('/User/1/slot1','exit',str(0))
        #screen.fill(r,50,70,100,100)
    if ir1==0 and result[1]["slot1"]["exit"]=="1" and result[1]["slot1"]["arrived"]=="0":
        firebase.put('/User/1/slot1','status',"not booked")
        firebase.put('/User/1/slot1','arrived',str(0))
        firebase.put('/User/1/slot1','exit',str(0))
        
    if result[1]["slot2"]["arrived"]=="1" and arrv2==0:
        print("servo up 2 ")
        p1.ChangeDutyCycle(7.5)
        time.sleep(1)
        arrv2=1
        text="Arrived at Gate 2         "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
        #servo up
        #p.ChangeDutyCycle(5)
    if result[1]["slot2"]["arrived"]=="1" and ir2==1:
        print("servo down 2")
        p1.ChangeDutyCycle(2.5)
        time.sleep(1)
        #p1.ChangeDutyCycle(7.5)
        text="Parked Slot 2          "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
        #screen.blit(asurf,(360,70))
        #servo down
        #p.ChnageDutyCycle(7.5)
        firebase.put('/User/1/slot2','arrived',str(2))
        #result[1]["slot2"]["arrived"]=2
    if result[1]["slot2"]["exit"]=="1" and exitup2==0 and result[1]["slot2"]["arrived"]=="2":
        print("servo up exit 2")#servo up
        exitup2=1
        #p1.ChangeDutyCycle(2.5)
        #time.sleep(1)
        p1.ChangeDutyCycle(7.5)
        time.sleep(1)
    if ir2==0 and result[1]["slot2"]["exit"]=="1" and result[1]["slot2"]["arrived"]=="2":
        print("servo down exit 2")
        p1.ChangeDutyCycle(2.5)
        time.sleep(1)
        #p1.ChangeDutyCycle(7.5) #servo down
        #time.sleep(1)
        #result[status,arrived,exit]=0
        arrv2=0
        exitup2=0
        firebase.put('/User/1/slot2','status',"not booked")
        firebase.put('/User/1/slot2','arrived',str(0))
        firebase.put('/User/1/slot2','exit',str(0))
    if ir2==0 and result[1]["slot2"]["exit"]=="1" and result[1]["slot2"]["arrived"]=="0":
        firebase.put('/User/1/slot2','status',"not booked")

import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servoPIN=13  #servo pin 1
GPIO.setup(servoPIN,GPIO.OUT) # servo 1
p = GPIO.PWM(servoPIN, 50) # GPIO 13 for PWM with 50Hz
p.start(2.5) # Initialization
p.ChangeDutyCycle(0)
servoPin2=26  # servo pin 2
GPIO.setup(servoPin2,GPIO.OUT)  #servo 2
p1= GPIO.PWM(servoPin2,50)    # GPIO 26 pWM 50Hz
p1.start(2.5)
p1.ChangeDutyCycle(0)

GPIO.setup(18,GPIO.OUT)  #led1
GPIO.setup(27,GPIO.OUT)  #led2
GPIO.setup(17,GPIO.IN)  # ir1
GPIO.setup(22,GPIO.IN)  #ir2 
from firebase import firebase
firebase = firebase.FirebaseApplication('https://parkingsystem-4f32e.firebaseio.com/',None)
GPIO.output(18,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
arrv=0
arrv2=0
exitup=0
exitup2=0
while True:
    #pygame.display.flip()
    #screen.blit(t2,(230,15))
    #pygame.draw.lines(screen,black,False,[(320,50),(320,300)],2)
    result=firebase.get('/User',None)
    #print result
    ir1=GPIO.input(17)
    ir2=GPIO.input(22)
    if result[1]["slot1"]["status"]=="booked" :
        GPIO.output(18,GPIO.LOW)
        text="Booked Slot 1"
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50))    
    else:
        GPIO.output(18,GPIO.HIGH)
        text="Free Slot 1               "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50)) 
    if result[1]["slot2"]["status"]=="booked" :
        GPIO.output(27,GPIO.LOW)
        text="Booked Slot 2"
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
    else:
        GPIO.output(27,GPIO.HIGH)
        text="Free Slot 2           "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
        
    if result[1]["slot1"]["arrived"]=="1" and arrv==0:
        print("servo up")
        p.ChangeDutyCycle(7.5)
        time.sleep(1)
        arrv=1
        text="Arrvied at Gate 1"
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50))
        #servo up
        #p.ChangeDutyCycle(5)
    if result[1]["slot1"]["arrived"]=="1" and ir1==1:
        print("servo down")
        p.ChangeDutyCycle(2.5)
        time.sleep(1)
        text="Parked Slot 1           "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(140,50))
        #screen.blit(asurf,(50,70))
        #servo down
        #p.ChnageDutyCycle(7.5)
        firebase.put('/User/1/slot1','arrived',str(2))
        #result[1]["slot1"]["arrived"]=2
    if result[1]["slot1"]["exit"]=="1" and exitup==0 and result[1]["slot1"]["arrived"]=="2":
        print("servo up exit")#servo up
        exitup=1
        p.ChangeDutyCycle(7.5)
        time.sleep(1)
    if ir1==0 and result[1]["slot1"]["exit"]=="1" and result[1]["slot1"]["arrived"]=="2":
        print("servo down exit")
        p.ChangeDutyCycle(2.5) #servo down
        time.sleep(1)
        #result[status,arrived,exit]=0
        arrv=0
        exitup=0
        firebase.put('/User/1/slot1','status',"not booked")
        firebase.put('/User/1/slot1','arrived',str(0))
        firebase.put('/User/1/slot1','exit',str(0))
        #screen.fill(r,50,70,100,100)
    if ir1==0 and result[1]["slot1"]["exit"]=="1" and result[1]["slot1"]["arrived"]=="0":
        firebase.put('/User/1/slot1','status',"not booked")
        firebase.put('/User/1/slot1','arrived',str(0))
        firebase.put('/User/1/slot1','exit',str(0))
        
    if result[1]["slot2"]["arrived"]=="1" and arrv2==0:
        print("servo up 2 ")
        p1.ChangeDutyCycle(7.5)
        time.sleep(1)
        arrv2=1
        text="Arrived at Gate 2         "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
        #servo up
        #p.ChangeDutyCycle(5)
    if result[1]["slot2"]["arrived"]=="1" and ir2==1:
        print("servo down 2")
        p1.ChangeDutyCycle(2.5)
        time.sleep(1)
        #p1.ChangeDutyCycle(7.5)
        text="Parked Slot 2          "
        #t=f1.render(text ,True,(255,0,0),(255,255,255))
        #screen.blit(t,(460,50))
        #screen.blit(asurf,(360,70))
        #servo down
        #p.ChnageDutyCycle(7.5)
        firebase.put('/User/1/slot2','arrived',str(2))
        #result[1]["slot2"]["arrived"]=2
    if result[1]["slot2"]["exit"]=="1" and exitup2==0 and result[1]["slot2"]["arrived"]=="2":
        print("servo up exit 2")#servo up
        exitup2=1
        #p1.ChangeDutyCycle(2.5)
        #time.sleep(1)
        p1.ChangeDutyCycle(7.5)
        time.sleep(1)
    if ir2==0 and result[1]["slot2"]["exit"]=="1" and result[1]["slot2"]["arrived"]=="2":
        print("servo down exit 2")
        p1.ChangeDutyCycle(2.5)
        time.sleep(1)
        #p1.ChangeDutyCycle(7.5) #servo down
        #time.sleep(1)
        #result[status,arrived,exit]=0
        arrv2=0
        exitup2=0
        firebase.put('/User/1/slot2','status',"not booked")
        firebase.put('/User/1/slot2','arrived',str(0))
        firebase.put('/User/1/slot2','exit',str(0))
    if ir2==0 and result[1]["slot2"]["exit"]=="1" and result[1]["slot2"]["arrived"]=="0":
        firebase.put('/User/1/slot2','status',"not booked")
        firebase.put('/User/1/slot2','arrived',str(0))
        firebase.put('/User/1/slot2','exit',str(0))    
                                      
            
            

        
        firebase.put('/User/1/slot2','exit',str(0))    
                                      
            
            

        

