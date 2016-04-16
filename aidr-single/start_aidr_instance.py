
import sys, time
import boto.ec2
import boto.route53

DRY_RUN = False
WAIT_INTERVAL = 60
AWS_REGION = 'ap-southeast-2'

# AIDR base installation on Ubuntu 14.04 server
AIDR_IMAGE_ID = 'ami-bcba98df'

# Ubuntu 14.04 server base image
#AIDR_IMAGE_ID = 'ami-6c14310f'

AIDR_INSTANCE_TYPE ='m4.large'
#AIDR_INSTANCE_TYPE ='t2.medium'

USER_DATA="""sudo apt-get install -y git
git clone https://github.com/burmesecloud/bcloud-infra-auto.git
sudo bcloud-infra-auto/aidr-single/install.sh
"""

conn = boto.ec2.connect_to_region(AWS_REGION)

# Check if there are existing AIDR instances
for res in conn.get_all_reservations():
	for i in  res.instances:
		if i.image_id == AIDR_IMAGE_ID and i.state in ('pending', 'running'):
			print "ERROR. There are existing AIDR instances."
			print "instance-id:", i.id
			print "private_dns_name:", i.private_dns_name
			print "public_dns_name:", i.public_dns_name
			print "ip_address:", i.ip_address
			print "state:", i.state
			sys.exit(1)

print "Starting new AIDR instance."

conn.run_instances(
	AIDR_IMAGE_ID,
    key_name='bcloud-key-1',
	instance_type=AIDR_INSTANCE_TYPE,
    security_groups=['bcloud-sg-1'],
	instance_initiated_shutdown_behavior='terminate',
	user_data = USER_DATA,
	dry_run=DRY_RUN)

# Wait until the instance has been assigned an ip address
ip_address = ''
while ip_address == '':

	# Give sometime for the instance to be ready
	for s in range(0, WAIT_INTERVAL):
		print "\rWaiting for", WAIT_INTERVAL-s, "seconds",
		sys.stdout.flush()
		time.sleep(1)
	print ""

	for res in conn.get_all_reservations():
		for i in  res.instances:
			if i.image_id == AIDR_IMAGE_ID and i.state in ('pending', 'running'):
				print "AIDR instance found."
				print "instance-id:", i.id
				print "private_dns_name:", i.private_dns_name
				print "public_dns_name:", i.public_dns_name
				print "ip_address:", i.ip_address
				print "state:", i.state
				ip_address = i.ip_address
				instance_found = True
				break

	if not instance_found:
		print "ERROR: There are no AIDR instances."
		sys.exit(1)

print "Setting domain name."

conn = boto.route53.connect_to_region(AWS_REGION)
zone = conn.get_zone("burmesecloud.net.")
change_set = boto.route53.record.ResourceRecordSets(conn, zone.id)
changes1 = change_set.add_change("UPSERT", "aidr.burmesecloud.net.", type="A", ttl=300)
changes1.add_value(ip_address)
change_set.commit()

print "Done."
