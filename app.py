from flask import Flask, render_template, request
import RPi.GPIO as GPIO

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Motor pins
IN1, IN2, IN3, IN4 = 2, 3, 4, 17
MOTOR_PINS = [IN1, IN2, IN3, IN4]

for pin in MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# PWM setup (for forward pins)
pwm_IN1 = GPIO.PWM(IN1, 100)  # 100 Hz
pwm_IN3 = GPIO.PWM(IN3, 100)
pwm_IN1.start(0)
pwm_IN3.start(0)

# Global speed
current_speed = 50

# Movement functions
def set_speed(speed):
    global current_speed
    current_speed = speed

def turn_left():
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_IN1.ChangeDutyCycle(current_speed)
    pwm_IN3.ChangeDutyCycle(current_speed)

def turn_right():
    pwm_IN1.ChangeDutyCycle(0)
    pwm_IN3.ChangeDutyCycle(0)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)

def forward():
    GPIO.output(IN2, GPIO.HIGH)
    pwm_IN3.ChangeDutyCycle(current_speed)
    GPIO.output(IN4, GPIO.LOW)
    pwm_IN1.ChangeDutyCycle(0)

def backward():
    pwm_IN1.ChangeDutyCycle(current_speed)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_IN3.ChangeDutyCycle(0)

def stop():
    pwm_IN1.ChangeDutyCycle(0)
    pwm_IN3.ChangeDutyCycle(0)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Flask setup
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def control():
    global current_speed
    if request.method == "POST":
        action = request.form.get("action")
        speed = request.form.get("speed")
        if speed:
            set_speed(int(speed))

        if action == "forward":
            forward()
        elif action == "backward":
            backward()
        elif action == "left":
            turn_left()
        elif action == "right":
            turn_right()
        elif action == "stop":
            stop()

    return render_template("index.html", speed=current_speed)

@app.route("/cleanup")
def cleanup():
    stop()
    GPIO.cleanup()
    return "GPIO Cleaned up"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
