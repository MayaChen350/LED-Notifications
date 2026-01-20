import subprocess
import threading
import RPi.GPIO as GPIO

# values on the breadboard or something
RED_PIN = 12
GREEN_PIN = 19
BLUE_PIN = 13

def parse_dbus_monitor_output(output: list[str]) -> None:
    def get_index() -> int:
        i = 0
        while i < len(output):
            if output[i].startswith('string "discord"'):
                return i
            else:
                    i += 1

        return -1

    index = get_index()

    if index == -1:
        return

    output = output[index:index+5]

    parsed = {
        "app_name": output[0].strip("string").strip(),
        "title": output[3].strip("string").strip(),
        "content": output[4].strip("string").strip(),
    }

    print(parsed["app_name"], "\n",  parsed["title"],"\n", parsed["content"], "\n",)

def listen_notifications():
    process = subprocess.Popen(["dbus-monitor", "interface='org.freedesktop.Notifications'"], stdout=subprocess.PIPE)
    lines = []
    for line in process.stdout:
        line = line.decode("utf-8").strip()
        lines.append(line)
        if line == "int32 -1":
            break

    parse_dbus_monitor_output(lines)

def main():
    # https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-a-RGB-LED/
    # disable warnings (optional)
    GPIO.setwarnings(False)
    # Select GPIO Mode
    GPIO.setmode(GPIO.BCM)
    # set pins as outputs
    GPIO.setup(redPin, GPIO.OUT)
    GPIO.setup(greenPin, GPIO.OUT)
    GPIO.setup(bluePin, GPIO.OUT)

    # Start the notification listener in a separate thread
    listener_thread = threading.Thread(target=listen_notifications, daemon=True)
    listener_thread.start()
    while True:
        pass

if __name__ == '__main__':
    main()
