from gpiozero import Servo
from time import sleep

steer = Servo(15)
go = Servo(14)

def goS():
    print('goS')
    go.value = 0.75
    sleep(1)
    go.value = 0

    
def left():
    print('inleft')
    steer.value = 0.75
    sleep(1)
    steer.value = 0
    
def right():
    print('inright')
    steer.value = -0.75
    sleep(1)
    steer.value = 0
    
def stop():
    print('stopped')
    steer.value = 0
    go.value = 0

while True:
    f = open('direction.txt',"r")
    content = f.read()
    print(content)
    if(content == 'left'):
        left()
    elif(content == 'right'):
        right()
    elif(content == 'straight'):
        goS()
    elif(content == 'stop'):
        stop()
    else:
        print("ERROR")
        

    

#try:
    #while True:
        #servo.value = 0.75 #left
        #sleep(1)
        #servo.value = 0
        #sleep(5)
