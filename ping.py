import socket, time,sys
oks=0
perc = []
pings = []

def getsr():
	global perc, pings
	percs, pingsc = 0, 0

	for i in perc:
		percs+=i

	for i in pings:
		pingsc+=i

	return round(pingsc/len(pings),3), round(percs/len(perc),3)

def ping(ip, port, timeout):
	global oks
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(timeout)

	st_time = time.time()
	
	try:
		s.connect((ip, port))
		lat = round(time.time()-st_time,3)*1000
		s.close()
		status = "OK"
		oks+=1
	except Exception as Ex:
		if oks >= 0:
			oks-=1
		else:
			oks = 0
		Ex = str(Ex).lower() 
		if "refused" in Ex or "reject" in Ex:
			status = "REFUSED"
		elif "read" in Ex or "broken pipe" in Ex:
			status = "READ_TIMED_OUT"
		elif "timed out" in Ex or "unreac" in Ex:
			status = "CONNECT_TIMED_OUT"
		else:
			status = Ex
		lat = -1

	

	return status, lat
args = sys.argv
if len(args) > 2:
	ip, port = args[1], int(args[2])
	try:
		timeout, delay = int(args[3]), int(args[4])
	except:
		timeout, delay = 3, 1

	seq = 1
	while True:
		try:
			state, latency = ping(ip, port, timeout)
			try:
				if oks >= seq:
					oksp = 100

				else:
					oksp = (oks*100)/seq
			except:
				oksp = 0
			
			if oksp <= seq:
				oksp = 0

			per = round(oksp,3)

			perc.append(per)
			pings.append(latency)

			print('[#{}] {}:{} => {} ({} MS) [{}% oks]'.format(seq, ip, port, state, latency, per))
			seq+=1
			time.sleep(delay)
		except:
			srms, srpc = getsr()

			print('\n\n | RESULT: (avg) {} ms | {} % oks'.format(srms, srpc))
			sys.exit(1)
else:
	print('    TCP PINGER\n   by Lonov\n\n | Usage: python3 ping.py [host] [port] [timeout|3] [delay|1]')