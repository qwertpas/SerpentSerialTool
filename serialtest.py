import asyncio
import serial

async def read_serial():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            print("New message:", data)
        await asyncio.sleep(0.1)

# Open the serial port
ser = serial.Serial('/dev/cu.usbmodem109297901', 9600)  # Replace 'COM1' with the appropriate port and '9600' with the baud rate

# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Run the serial reading coroutine concurrently
serial_task = loop.create_task(read_serial())

# Perform other operations concurrently (example)
async def other_operation():
    while True:
        print("Performing other operation...")
        await asyncio.sleep(1)

other_operation_task = loop.create_task(other_operation())

# Run the event loop
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Cancel the tasks and close the event loop
serial_task.cancel()
other_operation_task.cancel()
loop.close()
