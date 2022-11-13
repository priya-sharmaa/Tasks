#!/bin/bash

echo "Downloading the version file from S3"
aws s3 cp s3://dashboard-static-assets/personalization-ui/editor/version.json .
if [ "$?" -ne "0" ]; then
  echo "Download error"
  exit 1
else
  echo "Successfully Downloaded the version file from bucket"
fi
echo "Displaying before change"
cat version.json
#############################################################
echo "Displaying user input values"
echo "Dcname: ${DCName}"
echo "Version Value: ${VersionValue}"
cat version.json | jq --arg k "${DCName}" --arg v "${VersionValue}" '.[$k]  = $v' > version1.json && mv version1.json version.json
if [ "$?" -ne "0" ]; then
  echo "Version Changed Errorr"
  exit 1
else
  echo "Successfully Changed the version file of S3 bucket"
fi
echo "Displaying after change"
cat version.json
if grep -q "\"${DCName}\": \"${VersionValue}\"" version.json
then
     echo "Version updated"
else
  echo "Not updated, exited"
  exit 1
fi
#############################################################
echo "Uploading the updated file back to S3"
aws s3 cp version.json s3://dashboard-static-assets/personalization-ui/editor/version.json
if [ "$?" -ne "0" ]; then
  echo "Upload error"
  exit 1
else
  echo "Successfully Uploaded the version file back to S3"
fi
echo "Updating the permission"
aws s3api put-object-acl --bucket dashboard-static-assets --key personalization-ui/editor/version.json --grant-full-control id="cdd2c7d11f6a44578eeaa5d283d8b72c936691695e41c52a58534cb54e71c0fb" --grant-read uri="http://acs.amazonaws.com/groups/global/AllUsers"
echo "$?"
echo "Permission updated successfully"
#############################################################
#echo "Invalidating the path in cloudfront"
aws cloudfront create-invalidation --distribution-id EKNH03VBDKTPF --paths "/personalization-ui/editor/version.json"
#Running while loop to check the success result of above command and exiting when gets 0
echo "$?"
i=0
while [ $i -lt 360 ];
do
if [ "$?" -ne "0" ]; then
  echo "Invalidating error"
  exit 1
else
  echo "Successfully Invalidated the path of version file in cloudfront"
  break
fi
sleep 10s;
done
##############################################################
echo "Displaying and checking the updated file content from cloudfront"
curl https://app-cdn.moengage.com/personalization-ui/editor/version.json
#sleep 120s
curl https://app-cdn.moengage.com/personalization-ui/editor/version.json -o versionnew.json
if grep -q "\"${DCName}\": \"${VersionValue}\"" versionnew.json
then
     echo "Cloud Front Invalidated with old version"
else
  echo "Cloud Front not Invalidated with old version"
  exit 1
fi
#sleep 30s
#curl https://app-cdn.moengage.com/personalization-ui/editor/version.json

