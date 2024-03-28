import socket
from messager import messager, RequestError
import sys
import struct

def determine_ip_type(hostname):
    ip_address = socket.getaddrinfo(hostname, None)[0][4][0]
    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        return socket.AF_INET
    except socket.error:
        pass

    try:
        socket.inet_pton(socket.AF_INET6, ip_address)
        return socket.AF_INET6
    except socket.error:
        pass

    # If neither conversion succeeds, the resolved IP address is not a valid IPv4 or IPv6 address
    return None

def get_address_family_string(address_family):
    if address_family == socket.AF_INET:
        return "IPv4"
    elif address_family == socket.AF_INET6:
        return "IPv6"
    else:
        return "Unknown"

def main():
    # Check if at least three arguments are provided (host, port, and command)
    if len(sys.argv) < 4:
        print("Usage: python client.py <host> <port> <command>")
        return

    # Extract host and port from command-line arguments
    host = str(sys.argv[1]).strip()
    port = int(sys.argv[2])
    program_type = sys.argv[3]
    

    try: # Test if the program_type is valid
        messager_obj = messager(program_type=program_type)
    except Exception as e:
        raise e

    # Provided arguments
    print("Host:            ", host)
    print("Port:            ", port)
    print("P type:          ", program_type)
    print("Connect using:   ", get_address_family_string(determine_ip_type(host)))
    print()

    # print(socket.inet_pton(socket.AF_INET,host))


    # Creating the socket object
    s = socket.socket(
        determine_ip_type(host),    # IPv6 
        socket.SOCK_DGRAM   # UDP
        )

    s.settimeout(404)

    # Try to connect with server and send a packet
    try:
        s.connect((host, port))
        print("Connected successfully!")

        packet = messager_obj.request(sys.argv[4:])
        print(f"Packet bytes: {struct.unpack(messager_obj.packet_format,packet)}\n")

        # Send the packet to the server
        s.sendto(packet, (host, port))

        # Receive response from the server
        response, addr = s.recvfrom(4000)

        try: # Sanity test, if the an Error is provided by the server, the program stops
            messager_obj.check_error_message(response)

        except RequestError as e:
            raise e 
        
        # If isin't a error message, continue
        print(f"{len(response)} Packets recieved!")
        print("Response from server:", messager_obj.response(response))
        
    except socket.timeout:
        print("Timeout: No response received from the server. Resending request...")
        # Resend the request
        s.sendto(packet, (host, port))

    except Exception as e:
        print("Connection failed:", e)
        raise e

    print("-"*150)
    # Closing the socket object
    s.close()

if __name__ == "__main__":
    main()