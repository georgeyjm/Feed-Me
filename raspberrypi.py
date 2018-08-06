import time
from RPi import GPIO
from picamera import PiCamera
import requests

# Initialize RaspberryPi Pin
ULTRASOUND_TRIGGER = 23
ULTRASOUND_ECHO = 24
STEERS = (11, 7, 13)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Initialize Ultrasound Pins
GPIO.setup(ULTRASOUND_TRIGGER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ULTRASOUND_ECHO, GPIO.IN)
ultrasound_pwm = GPIO.PWM(ULTRASOUND_TRIGGER, 50)
ultrasound_pwm.start(0)

# Initialize Steerings
steer_pwms = []
for i in STEERS:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
    pwm = GPIO.PWM(i, 50)
    steer_pwms.append(pwm)
    pwm.start(0)

# Initialize Camera
camera = PiCamera()
# camera.resolution = (299, 299)

# Steering Indices of Categories
# '1': recyclable
# '2': nonrecyclable
# '3': toxic
DOOR_INDEX = {'1': 0, '2': 1, '3': 2, '4': 0}

PREDICT_URL = 'http://feedme.georgeyu.cn:8000/predict'
SOUND_URL = 'http://10.200.4.90:8000/play'


def toggle_door(category, state):
    state = state in (True, 1, 'open')
    angle = (0, 180)[state]
    index = DOOR_INDEX[category]
    door = STEERS[index]
    pwm = steer_pwms[index]

    duty = angle / 18 + 2
    GPIO.output(door, GPIO.HIGH)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    requests.get(SOUND_URL)
    GPIO.output(door, GPIO.LOW)
    pwm.ChangeDutyCycle(GPIO.LOW)


def get_dist():
    GPIO.output(ULTRASOUND_TRIGGER, GPIO.HIGH)
    time.sleep(0.0015) # empirical value?
    GPIO.output(ULTRASOUND_TRIGGER, GPIO.LOW)

    while not GPIO.input(ULTRASOUND_ECHO):
        pass
    start = time.time()
    while GPIO.input(ULTRASOUND_ECHO):
        pass
    end = time.time()
    # dist = (end - start) * 340 * 100 / 2
    dist = (end - start) * 17000
    time.sleep(0.05)
    return dist


while True:
    print(get_dist())
    if get_dist() < 18 and get_dist() < 18:
        # time.sleep(0.1)
        # print('object')
        camera.capture('image.jpg')
        # start = time.time()
        obj, recyclable = requests.post(PREDICT_URL, files={'image': open('image.jpg', 'rb')}).json()
        # print(time.time() - start, 's')
        # most = sorted(req.keys(), key=lambda x: req[x])[0]
        print(obj, recyclable)
        toggle_door(recyclable, 'open')
        time.sleep(2)
        toggle_door(recyclable, 'close')

