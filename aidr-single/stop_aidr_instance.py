
import sys, time
import boto.ec2

DRY_RUN=False
AWS_REGION = 'ap-southeast-2'

# AIDR base installation on Ubuntu 14.04 server
AIDR_IMAGE_ID = 'ami-bcba98df'

conn = boto.ec2.connect_to_region(AWS_REGION)

print "Finding existing AIDR instances."
for res in conn.get_all_reservations():
	for i in  res.instances:

		if i.image_id == AIDR_IMAGE_ID and i.state == 'running':
			print ""
			print "AIDR instance found."
			print "instance-id:", i.id
			print "private_dns_name:", i.private_dns_name
			print "public_dns_name:", i.public_dns_name
			print "ip_address:", i.ip_address
			print "state:", i.state
			ip_address = i.ip_address
			ans = raw_input("Are you sure to stop and terminate this instance? (Y/n):")
			if ans == 'Y':
				i.stop()
				i.terminate()
				print "Instance terminated."

print "Finding existing AIDR instances again."
for res in conn.get_all_reservations():
	for i in  res.instances:
		if i.image_id == AIDR_IMAGE_ID and i.state == 'running':
			print "ERROR. There are AIDR instances still running."
			print "instance-id:", i.id
			print "private_dns_name:", i.private_dns_name
			print "public_dns_name:", i.public_dns_name
			print "ip_address:", i.ip_address
			print "state:", i.state
			sys.exit(1)
else:
	print "There are no AIDR instances running at this time."
