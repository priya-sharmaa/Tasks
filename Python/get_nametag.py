import boto3

def get_boto3_client():
         #region = self.region
         # Dummy Credentials
         return boto3.client("ec2",
                             aws_access_key_id="Value",
                             aws_secret_access_key="Value",
                             region_name="Value"
                             )
#give the values of the instance id get from csv file
instanceidlist= ["instance id", "instance id", "instance id"]

#to get the name of instances by providing instance id
def get_tag_name(instanceid):
    client = get_boto3_client()
    tags = client.describe_tags( 
        Filters=
        [
            {'Name': 'resource-id', 'Values': [instanceid, ], 
            }, 
        ],
        )
    resourceName=""
    for tag in tags['Tags']:
        #change the Name to Business to get the business tag value
        if tag['Key'] == 'Name':
            print(tag['Value'])

    return None



def Call():
    for i in instanceidlist:

        get_tag_name(i)

Call()
