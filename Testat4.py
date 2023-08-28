import RPi.GPIO as GPIO
import time
import sqlite3

taster_pin = 17
led_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(taster_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(led_pin, GPIO.OUT)
led_status = False

conn = sqlite3.connect('led_status.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS led_status
                (id INTEGER PRIMARY KEY AUTOINCREMENT, status INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def update_led_status(status):
    GPIO.output(led_pin, status)
    cursor.execute('INSERT INTO led_status (status) VALUES (?)', (int(status),))
    conn.commit()

try:
    while True:
        taster_status = GPIO.input(taster_pin)

        if taster_status == GPIO.HIGH:
            if led_status:
                led_status = False
                update_led_status(led_status)
                time.sleep(0.2)  
            else:
                led_status = True
                update_led_status(led_status)
                time.sleep(0.2)  

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  
    conn.close()   