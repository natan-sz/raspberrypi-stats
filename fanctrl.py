#!/usr/bin/python

import RPi.GPIO as GPIO

FAN_PIN = 21
PWM_FREQ = 25

class FanController:
    def __init__(self):
        self.freq = 50
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FAN_PIN, GPIO.OUT)

        self.pwm = GPIO.PWM(FAN_PIN, PWM_FREQ)
        self.pwm.start(self.freq)


    def changeFrequency(self,freq):
        self.pwm.ChangeDutyCycle(freq)
        self.freq = freq
