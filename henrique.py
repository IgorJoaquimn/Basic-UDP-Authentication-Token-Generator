import socket
host = "slardar.snes.2advanced.dev"
port = 51001
# Creating the socket object
s = socket.socket(
    socket.AF_INET,    # IPv6 
    socket.SOCK_DGRAM   # UDP
    )

s.settimeout(404)

# Try to connect with server and send a packet
try:
    s.connect((host, port))
    print("Connected successfully!")
except Exception as e:
    print("ERROR !", e)




# Closing the socket object
s.close()
