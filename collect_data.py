import time
from datetime import datetime
import board
import adafruit_mpu6050
from gpiozero import LED, Button
from RPLCD.i2c import CharLCD

i = 0

def run():
	# From wiring diagram
	global i
	record_led = LED(9)
	write_led = LED(8)
	start_stop_btn = Button(23)
	lcd_btn = Button(6)
	lcd = CharLCD('PCF8574', 0x27)

	i2c = board.I2C()  # uses board.SCL and board.SDA
	mpu = adafruit_mpu6050.MPU6050(i2c)
	record_data = False
	lcd_state = -1

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

			if(lcd_btn.value == 1 and not lcd_btn.is_held):
				i = 100
				lcd.clear()
				lcd_state += 1
				if (lcd_state > 7):
					lcd_state = 0

			if(i > 2):
				lcd.clear()
				write_lcd(accel, gyro, temp, lcd, lcd_state)
				i = 0

			i += 1

		else:
			lcd.clear()
			lcd.write_string('Recording data')
			lcd.cursor_pos = (1,0)
			lcd.write_string('OFF')
			lcd_state = 0 
			record_led.off()
			time.sleep(1)

def write_lcd(accel, gyro, temp, lcd, lcd_state):
	if(lcd_state == 1):
		lcd.write_string('Acceleration: X\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(accel[0], 8)))
	elif(lcd_state == 2):
		lcd.write_string('Acceleration: Y\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(accel[1], 8)))
	elif(lcd_state == 3):
		lcd.write_string('Acceleration: Z\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(accel[2], 8)))
	elif(lcd_state == 4):
		lcd.write_string('Angular Vel: X\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(gyro[0], 8)))
	elif(lcd_state == 5):
		lcd.write_string('Angular Vel: Y\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(gyro[1], 8)))
	elif(lcd_state == 6):
		lcd.write_string('Angular Vel: Z\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(gyro[2], 8)))
	elif(lcd_state == 7):
		lcd.write_string('Temperature\n')
		lcd.cursor_pos = (1,0)
		lcd.write_string(str(round(temp, 8)))
	else:
		lcd.write_string('Recording data')
		lcd.cursor_pos = (1,0)
		lcd.write_string('ON')

if __name__ == "__main__":
	run()

