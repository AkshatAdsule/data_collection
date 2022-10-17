import time
from datetime import datetime
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
from gpiozero import LED, Button

# From wiring diagram
record_led = LED(9)
write_led = LED(8)
start_stop_btn = Button(23)

# setup IMU
mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ
)
mpu.configure() # Apply the settings to the registers.

record_data = False

# setup CSV file
file = open('data.csv', 'a')
file.truncate(0) # clear file
file.write("time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,magno_x,magno_y,magno_z,temp\n")

start_time = datetime.now()

while True:
    if(start_stop_btn.value == 1): #button pressed
        record_data = not record_data

    if(record_data):
        write_led.on()
        record_led.on()

        accel = mpu.readAccelerometerMaster()
        gyro = mpu.readGyroscopeMaster()
        magno = mpu.readMagnetometerMaster()
        temp = mpu.readTemperatureMaster()

        time.sleep(0.125)
        write_led.off()
        time.sleep(0.125)

        csvline = ""
        now = datetime.now()
        current_time = now - start_time
        csvline += str(current_time)

        csvline += f",{accel[0]},{accel[1]},{accel[2]}"
        csvline += f",{gyro[0]},{gyro[1]},{gyro[2]}"
        csvline += f",{magno[0]},{magno[1]},{magno[2]}"
        csvline += f",{temp}\n"
        print(csvline,end='')
        file.write(csvline)
        file.flush()
    else:
        record_led.off()
        # time.sleep(0.25)