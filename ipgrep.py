#!/usr/bin/env python
import sys, re, socket, struct

cidr_re = re.compile(r"(\d+\.\d+\.\d+\.\d+(?:/\d+){0,1})")

def check_ip(a, b):

	a_parts = a.split('/',2)
	a_ip = struct.unpack('>I',socket.inet_aton(a_parts[0]))[0]
	a_mask = 32
	if len(a_parts) > 1:
		a_mask = int(a_parts[1])

	b_parts = b.split('/',2)
	b_ip = struct.unpack('>I',socket.inet_aton(b_parts[0]))[0]
	b_mask = 32
	if len(b_parts) > 1:
		b_mask = int(b_parts[1])

	roll = a_mask
	if b_mask < a_mask:
		roll = b_mask

	a_ip = a_ip >> (32 - roll) << (32 - roll);
	b_ip = b_ip >> (32 - roll) << (32 - roll);
	
	#print "{0} {1} {2} {3}".format(a_ip, a_mask, b_ip, b_mask)

	if a_ip == b_ip:
		return True
	
	return False

if len(sys.argv) < 3:
	print "{0} <cidr> <file> [file...]".format(sys.argv[0])
	sys.exit(0)

for filename in sys.argv[2:]:
	fd = open(filename)
	for line in fd:
		matches = False

		match = cidr_re.search(line)
		if match:
			for ip in match.groups():
				try:
					if check_ip(sys.argv[1], ip):
						matches = True
				except:
					pass
		if matches:
			if len(sys.argv) > 3:
				print "{0}: {1}".format(filename,
					line.rstrip("\n"))
			else:
				print line.rstrip("\n")
	fd.close()
