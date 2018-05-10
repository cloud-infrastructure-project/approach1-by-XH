#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError

#-----------------------------------------------
# create an IAM user:  
try:
    iam = boto3.client('iam')
    user = iam.create_user(UserName='xh3')
    print "Created user: %s" % user
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print "User already exists"
    else:
        print "Unexpected error: %s" % e


#-----------------------------------------------

def launch_an_instance():
    
    client = boto3.client(
        'ec2',
        aws_access_key_id= 'my-key',
        aws_secret_access_key= 'my-secret-acess-key',
        region_name= 'us-west-2'
        )
   
    filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}]
    response = client.describe_instances(Filters=filters)
    
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:           
            if instance["InstanceId"] and instance["State"]['Name'] == 'running': 
                #print instance
                print(instance["InstanceId"],instance["State"])
               
    print "Starting the instance..."
    instances = client.run_instances(    # ec2.create_instances   doesn't work, change to run work
        ImageId='ami-f2d3638a',#'ami-976152f2',#'ami-9be6f38c',  #The image id '[ami-9be6f38c]' does not exist,,, how to know which image are in the region
        MinCount=1,
        MaxCount=1,
        #KeyName='cloudtest',#"16:82:85:7e:16:58:1c:80:8c:48:90:30:9e:56:5b:bb:4d:e4:d1:6f",#'cloudtest',#
        InstanceType="t2.micro"
    )
    print "new running instance is \n"#, #instances#["InstanceId"],instance["State"]
    
    for instance in instances["Instances"]:           
        if instance["InstanceId"] and (instance["State"]['Name'] == 'running' or instance["State"]['Name'] == 'pending'): 
            print(instance["InstanceId"],instance["State"])
    return True
    
#-----------------------------------------------
def terminate_an_instance(instance_id):
    print "terminate_an_instance...", instance_id
    ec2 = boto3.resource('ec2')
   
    instance = ec2.Instance(str(instance_id))
    response = instance.terminate()
    
    if response:
        return True
    return False
#-----------------------------------------------
def get_instances_info():
    print "getting the info of instance..."
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            #print instance
            print(instance["InstanceId"],instance["State"])


#print 'done1'
#-----------------------------------------------
fail_str = 'We are sorry, there is a machine running.'
success_str = 'Congratuations, a machine has been created successfully.'

def launch_instance():
    result = launch_an_instance()
    print 'result: ',result
    if result:
        return success_str
    else:
        return fail_str
#-----------------------------------------------
def terminate_instance(instance_id):
    print("instance_id to be terminated: " + str(instance_id))
    result= terminate_an_instance(str(instance_id))
    print 'result: ',result
    if result:
        return 'Congratuations, a instance has been terminated successfully.'
    else:
        return 'Sorry, the terminate action is failed. -_-"'
#-----------------------------------------------
def instruction():
    print("Welcome to AWS EC2 ---- ")
    print("(a) get info of all instances")
    print("(b) create instance")
    print("(c) terminate instance")  
    print("(q) quit")


#print 'done2'
#-----------------------------------------------
if __name__ == "__main__":
    instruction()
    option = ''
    while (option != 'q'):
        option = raw_input('Please select your option: ')
        print 'option',option
        if option == 'b':
            #max_num_of_instance = raw_input('Please type the max number of instance: ')
            launch_instance()#(max_num_of_instance)
        elif option == 'c':
            instance_to_terminate = raw_input('Please select instance_to_terminate: ')
            print 'the input ',instance_to_terminate
            terminate_instance(instance_to_terminate)
        elif option == 'a':
            get_instances_info()
   

    print("Program Exited")


    #print 'done3'