dnslookup
=========

Course Project

The basic process of this program is the following:

 1. Obtain domain name from the command line input
 2. Obtain the target DNS server from the command line input
 3. Construct a UDP (DATAGRAM) socket 
 4. Construct a DNS query packet for the specific domain name, the type 
    of the query should be A.  (The types of queries is discussed in the 
    RFC, and this subject will be explained in class.)
 5. Send the query to the target DNS server using UDP socket.
 6. Wait for the response to be returned from the server.
 7. If a reply comes back in 5 seconds, interpret the response and output 
    the result to STDOUT, and then quit the program.
 8. If no reply comes back in 5 seconds, generate an error message and then 
    quit the program.

python dnslookup.py "DNS server IP" domainName -> e.q.: python dnslookup.py 8.8.8.8 www.cnn.com
send the domain name: www.cnn.com to the DNS Server: 8.8.8.8 at port 53 and get the IP address with other information.
