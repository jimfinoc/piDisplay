import serial
import time

# Configure the serial port
# For Raspberry Pi 3/4/Zero W, use '/dev/ttyS0' or '/dev/serial0'
# For older Pis (Pi 1, Pi 2, Pi Zero), use '/dev/ttyAMA0'
SERIAL_PORT = '/dev/ttyS0' 
BAUDRATE = 9600

try:
    # Open the serial port
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # Timeout for read operations
    )
    print(f"Serial port {SERIAL_PORT} opened successfully.")

    # Send data
    def send_data(data):
        encoded_data = data.encode('utf-8')
        ser.write(encoded_data)
        print(f"Sent: {data}")

    # Receive data
    def receive_data():
        if ser.in_waiting > 0:
            received_bytes = ser.readline() # Read until newline or timeout
            try:
                decoded_data = received_bytes.decode('utf-8').strip()
                print(f"Received: {decoded_data}")
                return decoded_data
            except UnicodeDecodeError:
                print(f"Received non-UTF-8 data: {received_bytes}")
        return None

    # Main loop for continuous TX/RX
    counter = 0
    while True:
        # message_to_send = f"Hello from Pi! Counter: {counter}"
        # send_data(message_to_send)
        time.sleep(1) # Wait for a second

        received_message = receive_data()
        if received_message:
            # Process received message if needed
            print(f"Processing received message: {received_message}")
            # pass

        counter += 1
        time.sleep(1) # Wait before next cycle

except serial.SerialException as e:
    print(f"Error opening or communicating with serial port: {e}")
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
