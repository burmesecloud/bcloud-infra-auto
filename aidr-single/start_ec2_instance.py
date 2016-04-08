
import sys, time
import boto.ec2

DRY_RUN=False
WAIT_TIME=180

USER_DATA="""sudo apt-get install -y git
git clone https://github.com/burmesecloud/bcloud-infra-auto.git
sudo bcloud-infra-auto/aidr-single/install.sh
"""

conn = boto.ec2.connect_to_region("ap-southeast-2")

print "Starting new ec2 instance."

conn.run_instances(
	#Ubuntu Server 14.04 LTS (PV),EBS General Purpose (SSD) Volume Type
	'ami-6c14310f',	
        key_name='bcloud-key-1',
        instance_type='t2.medium',
        security_groups=['bcloud-sg-1'],
	instance_initiated_shutdown_behavior='terminate',

	user_data = USER_DATA,
	dry_run=DRY_RUN)

for s in range(0, WAIT_TIME):
	print "\rWaiting for", WAIT_TIME-s, "seconds",
	sys.stdout.flush()
	time.sleep(1)

res = conn.get_all_reservations()[0]

for i in  res.instances:
	print "\n"
	print "instance-id:", i.id
	print "private_dns_name:", i.private_dns_name
	print "public_dns_name:", i.public_dns_name
	print "ip_address:", i.ip_address

raw_input("Press ENTER to terminate all instances when ready.")
res.stop_all(dry_run=DRY_RUN)
