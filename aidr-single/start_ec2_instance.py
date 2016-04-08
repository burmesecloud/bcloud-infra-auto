
import boto.ec2
conn = boto.ec2.connect_to_region("ap-southeast-2")

res = conn.run_instances(
	#Ubuntu Server 14.04 LTS (PV),EBS General Purpose (SSD) Volume Type
	'ami-6c14310f',	

        key_name='bcloud-key-1',
	
	#$0.08 per Hour
        instance_type='t2.medium',

        security_groups=['bcloud-sg-1'])
