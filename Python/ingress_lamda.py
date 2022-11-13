import json
import boto3
import urllib3

# TODO implement
def send_slack_notification(text1):

    payload = {
        "text": text1
    }
    http = urllib3.PoolManager()

    response = http.request(
        'POST', "slack web hook url",
        body = json.dumps(payload),
        headers = {'Content-Type': 'application/json'},
        retries = False)

def lambda_handler(event, context):
    event1 = event['detail']
    print(event1)
    eventname=event1['eventName']
    print(eventname)
    if eventname == 'AuthorizeSecurityGroupIngress':
        rp=event1['requestParameters']
        groupid=rp['groupId']
        print(rp)
        ipdetails=rp['ipPermissions']
        print(ipdetails)
        rp2=event1['responseElements']
        sgrdetail=rp2['securityGroupRuleSet']
        for itr in sgrdetail['items']:
            sgrid=itr['securityGroupRuleId']
            gid=itr['groupId']
            fromport=itr['fromPort']
            toport=itr['toPort']
            ip=itr['cidrIpv4']
            print(sgrid)
            if (ip=='0.0.0.0/0' and fromport!=443):
                text1="SG Id:" + str(gid) + "\n" + "SGR ID:" + str(sgrid) + "\n"+ "From Port:" + str(fromport) + "\n" + "Ip Address:" + str(ip)
                print(text1)
    
    if eventname == 'ModifySecurityGroupRules':
        rp3=event1['requestParameters']
        msgr=rp3['ModifySecurityGroupRulesRequest']
        sgrid2=msgr['SecurityGroupRule']['SecurityGroupRuleId']
        ip1=msgr['SecurityGroupRule']['SecurityGroupRule']['CidrIpv4']
        fromp=msgr['SecurityGroupRule']['SecurityGroupRule']['FromPort']
        gidd=msgr['GroupId']
        if (ip1=='0.0.0.0/0' and fromp!=443):
            text1="SG Id:" + str(gidd) + "\n" + "SGR ID:" + str(sgrid2) + "\n"+ "From Port:" + str(fromp) + "\n" + "Ip Address:" + str(ip1)
            print(text1)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
