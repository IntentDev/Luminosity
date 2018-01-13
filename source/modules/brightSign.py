def Send(MESSAGE):

	import socket
	
	UDP_IP = "255.255.255.255"
	UDP_PORT = 5000

	print("UDP Target IP: ", UDP_IP)
	print("UDP Port: ", UDP_PORT)
	print("udp message ", MESSAGE)
	
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP,UDP_PORT))