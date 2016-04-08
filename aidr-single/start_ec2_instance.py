
import sys, time
import boto.ec2

DRY_RUN=False

conn = boto.ec2.connect_to_region("ap-southeast-2")

print "Starting new ec2 instance."

res = conn.run_instances(
	#Ubuntu Server 14.04 LTS (PV),EBS General Purpose (SSD) Volume Type
	'ami-6c14310f',	

        key_name='bcloud-key-1',
	
        instance_type='t2.medium',

        security_groups=['bcloud-sg-1'],

	dry_run=DRY_RUN)

for s in range(0, 60):
	print "\rWaiting for", 60-s, "seconds",
	sys.stdout.flush()
	time.sleep(1)

for i in  res.instances:
	print "\ninstance-id:", i.id

raw_input("Press ENTER to terminate instance when ready.")
res.stop_all(dry_run=DRY_RUN)
