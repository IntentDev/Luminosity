def Send(address, port, message):

	import socket
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(bytes(message, "utf-8"), (address, port))