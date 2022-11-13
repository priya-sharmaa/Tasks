import boto3
regions = ['us-east-1']
instances = {}
data = ""

def get_all_instances(region):
    ec2_client = boto3.client("ec2", region_name=region)
    response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            try:
                flag = False
                for tag in instance['Tags']:
                    if tag['Key'] == 'aws:autoscaling:groupName':
                        flag = True
                    if tag['Key'] == 'Backup' and tag['Value'] == 'MongoDB':
                        flag = True
                if not flag:
                    user = 'ubuntu'
                    if instance['KeyName'] not in instances:
                        instances[instance['KeyName']] = []
                    instances[instance['KeyName']].append({'region': region, 'InstanceId': instance['InstanceId'], 'KeyName': instance['KeyName'], 'PrivateIpAddress': instance['PrivateIpAddress'], 'user': user})                        
            except:
                print(instance['InstanceId'])
    next_token = ''
    if 'NextToken' in response:
        next_token = response['NextToken']
    while next_token != '':
        response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}], NextToken=next_token)
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                try:
                    flag = False
                    for tag in instance['Tags']:
                        if tag['Key'] == 'aws:autoscaling:groupName':
                            flag = True
                        if tag['Key'] == 'Backup' and tag['Value'] == 'MongoDB':
                            flag = True
                    if not flag:
                        if instance['KeyName'] not in instances:
                            instances[instance['KeyName']] = []
                        instances[instance['KeyName']].append({'region': region, 'InstanceId': instance['InstanceId'], 'KeyName': instance['KeyName'], 'PrivateIpAddress': instance['PrivateIpAddress'], 'user': user})                        
                except:
                    print(instance['InstanceId'])
        next_token = ''
        if 'NextToken' in response:
            next_token = response['NextToken']

if __name__ == '__main__':
    for region in regions:
        get_all_instances(region)
    x = 1
    for instance in instances:
        data += '[server' + str(x) + ']\n'
        for i in instances[instance]:
            data += i['PrivateIpAddress'] + ' ansible_ssh_private_key_file=~/.ssh/' + i['KeyName'] + '.pem ansible_ssh_user=' + i['user'] + ' ansible_ssh_extra_args="-o IdentitiesOnly=yes"'+ '\n'
        data += '\n'
        x += 1
    file = open("hosts", "w")
    file.write(data)
    file.close()
    print(data)
