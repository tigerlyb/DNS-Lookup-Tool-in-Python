import socket
import sys
import struct

# construct the DNS query
def dnsquery(domain):
  d = ""
	for a in domain.split('.'):
		d = d + struct.pack("!b" + str(len(a)) + "s", len(a), a)
	
	l1 = "\x41\x41"
	l2 = "\x01\x00"
	l3 = "\x00\x01"
	l4 = "\x00\x00"
	l5 = "\x00\x00"
	l6 = "\x00\x00"
	header = l1 +l2 + l3 + l4 + l5 + l6
	q = d + "\x00\x00\x01\x00\x01"
	m = header + q
	#print "DNS query: ", m.encode("hex")
	return m

# send the DNS query to the DNS server using UDP
def Conn (ser, q):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(5)
		sock.sendto(q, ser)		
		data, addr = sock.recvfrom(1024)
	except Exception, e:
		print "No response from server", ser,e
		print "------------------------------------------------------"
		print ""
		sock.close()
		sys.exit()
	
	# get the messages from the server	
	severmessage = data.split(',', 0)
	#print "server message: ", severmessage
	
	reply = str(severmessage[0].encode("hex"))
	#print "Sever reply: ", reply	
		
	# get the RCODE field from the sever message
	rcode = reply[:8]
	rcode = rcode[7:]
	r = int(rcode)
	
	# check the RCODE with error detection 
	if (r == 0):	# no error, get the ip address	
		# check the ANCOUNT to fine the number of answers
		ancount = reply[:16]
		ancount = ancount[12:]
		count = int(ancount)
		print "Number of Answers: ", count
		print ""
		
		# get the answer from the server reply
		answer = reply[2*len(q):]
		name = domainName
		for i in range(0, count):			
			print "Answer ", i+1, ": "
			
			# get the owner name from the answer
			n = answer[:4]
			#print "NAME: ", name
			answer = answer[4:]
			
			# get the TYPE from the answer
			t = answer[:4]
			if (t == "0001"):
				print "TYPE: A"
			elif (t == "0005"):
				print "TYPE: CNAME"
			else:
				print "TYPE: ", t
			answer = answer[4:]
			
			# get the CLASS from the answer
			c = answer[:4]
			if (c == "0001"):
				print "CLASS: IN"
			else:
				print "CLASS: ", c
			answer = answer[4:]
			
			# get the TTL from the answer
			ttl = answer[:8]
			print "TTL: ", int(ttl, 16), "seconds"
			answer = answer[8:]
			
			# get the RDLENGTH from the answer
			l = answer[:4]
			print "RDLENGTH: ", int(l, 16)
			answer = answer[4:]
			
			# get the RDATA from the answer
			rdata = answer[:int(l, 16)*2]
			answer = answer[int(l, 16)*2:]
			
			if (t == "0001"): # get the IP from the RDATA if the TYPE is A			
				a = int(rdata, 16)		
				ip4 = a & 0xff
				a = a >> 8
				ip3 = a & 0xff
				a = a >> 8
				ip2 = a & 0xff
				a = a >> 8
				ip1 = a & 0xff
				print "IP: " + str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4)
				print ""
			else: # get the CNAME from the RDATA if the TYPE is CNAME				
				cname = ""
				rdata = rdata[2:]
				# print the CNAME
				for i in range(int(l, 16)-3):
					#print "RDATA: ", rdata					
					n = rdata[:2]
					n = int(n, 16)	
					rdata = rdata[2:]									
					if n <= 32:
						cname = cname + "."											
					cname = cname + chr(n)					
				print "CNAME: ", cname
				print ""
				#name = cname
	elif (r == 1):
		# error
		print "*** Format error: the name server was unable to interpret the query."
	elif (r == 2):
		# error
		print "*** Server failure: the name server was unable to process this query due to a problem with the name server."
	elif (r == 3):
		# error
		print "*** None exist domains: server can not find answer."
	elif (r == 4):
		# error
		print "*** Not Implemented: the name server does not support the requested kind of query."
	elif (r == 5):
		# error
		print "*** Server Refused."
	else:
		# error
		print "*** Other errors"
	
	print "------------------------------------------------------"
	print ""
	sock.close()
	
	
if __name__ == '__main__':

	serverIP = sys.argv[1]
	domainName = sys.argv[2]
	server = (serverIP, 53)
	print ""
	print "-------------------------------------------------"
	print "DNS server IP: \t", server
	print "Domain Name: \t", domainName
	print ""
	query = dnsquery(domainName)
	Conn(server, query)
