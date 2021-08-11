from cohesity_management_sdk.cohesity_client import CohesityClient
import getpass

class CohesityUserAuthentication(object):
    
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_ip = "10.26.1.174"
        self.username = "admin"
        self.password = "Cohe$1ty"
        self.domain = "local"
        
        # self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ") 
        # self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):     
      return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)
  
  
def main():
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    protection_run = cc.protection_runs.get_protection_runs()
    print(protection_run)
#run main function
if __name__ == '__main__':
    main()
  