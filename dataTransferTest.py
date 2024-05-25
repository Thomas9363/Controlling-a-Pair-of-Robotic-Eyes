import bluetooth
# Create a Bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# Set the port number for the server socket
port = 27
server_sock.bind(("", port))
# Listen for incoming connections from clients
server_sock.listen(1)
# Accept the client connection
client_sock, address = server_sock.accept()
print("Conexion realizada con:", address)
# Initialize a list to store data received in 255-based groups
dataIn = [255, 0, 100, 100]
# Initialize an index to keep track of dataIn elements
array_index = 0

while True:
    try:
        # Receive data from the client
        data = client_sock.recv(1024)
         # Convert the received data (bytes) to an integer       
        in_byte = int.from_bytes(data, byteorder='big') 
        # If the received byte is 255, it indicates the start of a new group
        if in_byte == 255:
            array_index = 0
        dataIn[array_index] = in_byte
        array_index += 1

        if array_index == 4:
            print("divide:", dataIn[0],"button:", dataIn[1],"X:", dataIn[2],"Y:", dataIn[3]  )
            print()
        # Ensure array_index does not exceed the length of dataIn
        array_index %= len(dataIn)
    except IOError:
        break
# Close the client and server sockets    
client_sock.close()
server_sock.close()    
