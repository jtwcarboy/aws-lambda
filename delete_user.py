import boto3
iam = boto3.client('iam')
 
def lambda_handler(event, context):
     USER_TO_DELETE = ['USER1']
     for UDEL in USER_TO_DELETE:
        List_of_Policies =  iam.list_user_policies(UserName=UDEL)
        print ("")
        print("********************")
        print ("If User has In-Line Policies then you need to remove them before running this")
        print ("We dont use in-line policies currently, permissions should be added at group level only ")
        print("********************")
        print ("Below you can see list of in-line policies if any")
        print (List_of_Policies)
   #     for key in List_of_Policies['PolicyNames']:
   #         print("Here is a list of all the policies attached")
    #        print (key['PolicyName'])
    #        myList = []
    #        myList.append(key['PolicyName'])
    #        val= len(myList)
    #        print (val)
    #        if val > 0:
    #            response = client.delete_user_policy(
    #            UserName=UDEL,
    #            PolicyName=(key['PolicyName'])
#)
        #    print(*myList, sep='\n')
            
        List_of_Groups =  iam.list_groups_for_user(UserName=UDEL)
        for key in List_of_Groups['Groups']:
            print("Here is a list of all groups")
            print (key['GroupName'])
            myList = []
            myList.append(key['GroupName'])
            print(*myList, sep='\n')
            response = iam.remove_user_from_group(
            GroupName=(key['GroupName']),
            UserName=UDEL
)
        List_of_MFA_Devices = iam.list_mfa_devices(UserName=UDEL)['MFADevices']
        for key in List_of_MFA_Devices:
             mfa_id = key['SerialNumber']
             print("Here is a list of all MFA")
             print (mfa_id)
             myList = []
             myList.append(mfa_id)
             print(*myList, sep='\n')
             response = iam.deactivate_mfa_device(
             UserName=UDEL,
             SerialNumber=mfa_id
)
     ##delete login profile first  
     response = iam.delete_login_profile(
     UserName=UDEL
)

     #then delete access keys
     access_keys = iam.list_access_keys(UserName=UDEL)['AccessKeyMetadata']
     for access_key in access_keys:
            print("Here is a list of all the Access Keys")
            access_key_id = access_key['AccessKeyId']
            print(access_key_id)
            response = iam.delete_access_key(
     AccessKeyId=access_key_id,
     UserName=UDEL
)
            
    #then delete account
     response = iam.delete_user(
     UserName=UDEL
)

   
