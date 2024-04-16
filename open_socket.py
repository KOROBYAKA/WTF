import socket

#Opens UDP socket
def open_UDP(UDP_PORT_NUMBER, IP_ADDR):
    while True:
        try:
            UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#AF_INET is for IPv4 protocol Address Falimly
                                                                        #SOCK_DGRAM for User Datagram Protocol
            break
        except:
            print(f'Port number {UDP_PORT_NUMBER} is already in use, trying open {UDP_PORT_NUMBER+1}!!!')
            UDP_PORT_NUMBER += 1
    print(f'''UDP port successfully opened with, UDP port's number is {UDP_PORT_NUMBER}''')
    return UDP_SOCKET


    UDP_SOCKET.bind((IP_ADDR, UDP_PORT_NUMBER))
def close_UDP(UDP_NAME):
    try:
        UDP_NAME.close()
    except:
        print('Error while closing UDP socket')



