import time
from datetime import datetime
import board
import adafruit_mpu6050
from gpiozero import LED, Button

def run():
    # From wiring diagram
    record_led = LED(9)
    write_led = LED(8)
    start_stop_btn = Button(23)

    i2c = board.I2C()  # uses board.SCL and board.SDA
    mpu = adafruit_mpu6050.MPU6050(i2c)
    record_data = False

    # setup CSV file
    file = open('data.csv', 'a')
    file.truncate(0) # clear file
    file.write("time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp\n")

    start_time = datetime.now()
    while True:
        if(start_stop_btn.value == 1 and not start_stop_btn.is_held): #button pressed
            record_data = not record_data

        if(record_data):
            write_led.on()
            record_led.on()

            accel = mpu.acceleration
            gyro = mpu.gyro
            temp = mpu.temperature

            time.sleep(0.125)
            write_led.off()
            time.sleep(0.125)

            csvline = ""
            now = datetime.now()
            current_time = now - start_time
            csvline += str(current_time)

            csvline += f",{accel[0]},{accel[1]},{accel[2]}"
            csvline += f",{gyro[0]},{gyro[1]},{gyro[2]}"
            csvline += f",{temp}\n"
            print(csvline,end='')
            file.write(csvline)
            file.flush()
        else:
            record_led.off()
            time.sleep(1)

if __name__ == "__main__":
    run()