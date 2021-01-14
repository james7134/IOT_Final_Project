import RPi.GPIO as GPIO          
import time

in1 = 16
in2 = 18
en = 22
ser_1=11


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.output(16,GPIO.LOW)
GPIO.output(18,GPIO.LOW)
GPIO.setup(11,GPIO.OUT)
p=GPIO.PWM(22,500)
servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

p.ChangeDutyCycle(100)


while(1)
    time.sleep(2)

    GPIO.output(16,GPIO.HIGH)
    GPIO.output(18,GPIO.LOW)

    time.sleep(2)

    GPIO.output(16,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(2)
    servo1.ChangeDutyCycle(16)

    time.sleep(2)
    servo1.ChangeDutyCycle(2)

    #Clean things up at the end
servo1.stop()
GPIO.cleanup()


