import subprocess
from timeit import default_timer
import sys


'''
subprocess.call is blocking, Popen is non-blocking
'''

def whatweb_scan(host):

	fname = host.replace('.', '_') + '-whatweb.txt'

	res = subprocess.call([
		'/usr/bin/whatweb', 
		'-a', '3', 
		f'--log-verbose={fname}',
		host]) 

	return res

def nikto_scan(host):

	fname = host.replace('.', '_') + '-nikto.html'

	res = subprocess.call([
		'/usr/bin/nikto', 
		'-host', host, 
		'-port', '80,443', 
		'-timeout', '3',
		'-output' , fname])

	return res

def gobuster_scan(host):

	fname = host.replace('.', '_') + '-gobuster.txt'

	res = subprocess.call([
		'/usr/bin/gobuster',
		'dir',
		'-u', f'https://{host}', 
		'-w', '/usr/share/wordlists/dirb/big.txt', 
		'-o', fname])
		
	return res

def main():

	if len(sys.argv) <2:
		print("Please supply a host list.")
		print(f"Usage: {sys.argv[0]} <hosts.txt>")
		sys.exit(0)

	START_TIME = default_timer()

	count = 0
	with open(sys.argv[1]) as f:

		for host in f.readlines():
			
			whatweb_scan(host.strip())
			gobuster_scan(host.strip())
			nikto_scan(host.strip())

			count += 1


	# Calculate time taken & print.
	elapsed = default_timer() - START_TIME
	time_completed_at = "{:5.2f} seconds".format(elapsed)
	print(f"{count} host(s) processed in {time_completed_at}!")

main()