from gpiozero import Button, DistanceSensor
from time import sleep

btn_vert = Button(5)
btn_rouge = Button(27)

capteur = DistanceSensor(echo =12,
                         trigger = 17,
                         max_distance = 3)

while True:
    if btn_vert.is_pressed:
        print("vert")   
        sleep(0.5)

    if btn_rouge.is_pressed:
        print("rouge")    
        sleep(0.5)

    cm = capteur.distance * 100
    print("Distance: " + str(cm) + " cm")
    sleep(1)
