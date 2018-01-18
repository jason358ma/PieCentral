import serial;

meme = serial.Serial('COM5')
while True:
	print(meme.read().decode("utf-8"))