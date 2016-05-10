import RPi.GPIO as GPIO
import sys, os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if (GPIO.input(24) == GPIO.HIGH):
    os.system("python3 /home/pi/FC_datalogger/main.py --adc >/dev/null 2>&1 &")
    print("***RUNNING FUEL CELL DATALOGGER!***")
sys.exit()
