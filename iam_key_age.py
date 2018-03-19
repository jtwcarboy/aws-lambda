import boto3, json, time, datetime, sys
sns                     = boto3.client('sns')
iam = boto3.client('iam')

def lambda_handler(event, context):
    mylist = []
    mylist.append(str("Over 90 Day Key Limit Users Are: "))
    my_list=list()
    iam_all_users = iam.list_users(MaxItems=200)
    for user in iam_all_users['Users']:
        my_list.append(user['UserName'])
   
    userindex = 0
    for user in my_list:
        userindex += 1
        user_keys = []
        username = user
        res = iam.list_access_keys(UserName=username)
        accesskeydate = res['AccessKeyMetadata'][0]['CreateDate']
        accesskeydate = accesskeydate.strftime("%Y-%m-%d %H:%M:%S")
        currentdate = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        accesskeyd = time.mktime(datetime.datetime.strptime(accesskeydate, "%Y-%m-%d %H:%M:%S").timetuple())
        currentd = time.mktime(datetime.datetime.strptime(currentdate, "%Y-%m-%d %H:%M:%S").timetuple())
        active_days = (currentd - accesskeyd)/60/60/24 ### We get the data in seconds. converting it to days
        
        if active_days > 89:
           mylist.append(str(user))
           mylist.append(str(" , "))
    mylist.remove('USERTOIGNORE')
    #here you can list this stanza over and over to keep users out of the report
    ##mylist.remove('EXCEPTION USER 2')
    print ("List Print")
    print (mylist)
    print ("end of list print") 
    
            
    val= len(mylist)
    print (val)
    if val > 3:
        mylist.append(str(" Have these Users Login and rotate Access Keys ASAP"))
        str1 = ''.join(mylist)
        physicalString = str1
        response = sns.publish(
             TopicArn='arn:aws:sns:us-east-1:YOURACCTNUMBER:key_age_report',
             Message= physicalString,
             Subject='Key Age Report AWS',
    )
    else:
        print ("Only Service Accts")
     
