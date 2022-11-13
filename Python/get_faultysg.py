import os
import boto3
import csv

def get_boto3_client():
         #region = self.region
         # Dummy Credentials
         return boto3.client("ec2",
                             aws_access_key_id="Value",
                             aws_secret_access_key="Value",
                             region_name="Value")
         
sgfilter=set()
sgrfilter=set()
sg_filter_list=[]
sgr_filter_list=[]
list1=[]
list2=[]

instancefiltered={}

#function to filter out the instances having faulty group rules attached and appended to a dict
def get_running_instances():
    ec2_client = get_boto3_client()
    instances=""
    paginator = ec2_client.get_paginator('describe_instances')
    page_iterator = paginator.paginate()
    for pg in page_iterator:
            reservationlist=pg["Reservations"]
            for reservation in reservationlist:
                instance=reservation['Instances'][0]
                instanceid=instance["InstanceId"]
                securitygrouplist=instance['SecurityGroups']
                for securityGroup in instance['SecurityGroups']:
                    sgnew=securityGroup['GroupId']
                    #checking instances sg in filtered sg list having faulty details
                    if sgnew in sgfilter:
                        if sgnew not in instancefiltered:
                            instancefiltered[sgnew]=[]
                        instancefiltered[sgnew].append(instanceid)
                        
#function to get the SG Name when passed group id as paramater
def get_sg_name(groupid):
    ec2_client = get_boto3_client()
    response = ec2_client.describe_security_groups(GroupIds=[str(groupid)])
    sg= response["SecurityGroups"]
    for n in sg:
        name=n["GroupName"]
        print("GroupName:{}".format(name))
        return name

#function to revoke the sg rule out from sg if having faulty configuration
def revoke_sg_rule(groupid, ruleid):
    ec2_client = get_boto3_client()
    response = ec2_client.revoke_security_group_ingress(DryRun=True,
        GroupId=str(groupid),
        SecurityGroupRuleIds=[
        str(ruleid),
    ]
    )
    if response["Return"]==True:
        print("Success Removing")


#revoke_sg_rule("sg-002a0a96d45156279","sgr-0bc1c8625216c588a")

#stores the faulty sg rule detailed information in a csv file
def write_to_csv():
    with open('/Users/priyasharma/Documents/PythonCode/PythonBasic_AWS/ep3/SGRDetails4.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['Groupname ', 'GroupId ', 'RuleId ', 'IP ', 'PortNumber ', 'Instance IDs '])
        writer.writeheader()
        writer.writerows(list1)

#filter out the sg, sg rules having faulty configuration and appending it to set for later use
def get_security_group_rules():
    client = get_boto3_client()

    paginator = client.get_paginator('describe_security_group_rules')
    page_iterator = paginator.paginate()
    for pg in page_iterator:
        for ri in pg["SecurityGroupRules"]:
            ruleid=ri["SecurityGroupRuleId"]
            groupid=ri["GroupId"]
            if "CidrIpv4" in ri:
                ip=ri["CidrIpv4"]
                fromport=ri["FromPort"]
                outboundcheck=ri["IsEgress"]
                if(ip=='0.0.0.0/0' and fromport!=443 and fromport!=None and not(outboundcheck)) :
                    sgrfilter.add(ruleid)
                    sgfilter.add(groupid)
                    print("\n")
                    groupname=get_sg_name(ri["GroupId"])
                    print("GroupId:{}".format(ri["GroupId"]))
                    print("GroupruleId:{}".format(ruleid))
                    print("IP:{}".format(ip))
                    print("PortNumber:{}".format(ri["FromPort"]))
                    portno=ri["FromPort"]
                    #appending the whole details in a list
                    list1.append({'Groupname ': groupname, 'GroupId ': groupid, 'RuleId ':ruleid,'IP ':ip,'PortNumber ': portno, 'Instance IDs ':''})
                    #calling to remove the faulty group rule from the group
                    #revoke_sg_rule(ri["GroupId"], ruleid)

get_security_group_rules()
get_running_instances()

def addinstances():
   
    for l in list1:
        ins=""
        if l['GroupId '] in instancefiltered:
            for i in instancefiltered[l['GroupId ']]:
                ins+=i+" "
            l["Instance IDs "]=ins
            
addinstances()
write_to_csv()
