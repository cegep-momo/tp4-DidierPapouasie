from gpiozero import Button
from time import sleep

btn_vert = Button(17)
btn_rouge = Button(27)

while True:
    if btn_vert.is_pressed:
        print("vert")   
        sleep(0.5)

    if btn_rouge.is_pressed:
        print("rouge")    
        sleep(0.5)
