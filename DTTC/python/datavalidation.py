from cohesity_management_sdk.cohesity_client import CohesityClient
import getpass
import datetime

class CohesityUserAuthentication(object):
    
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_ip = "10.26.0.159"
        self.username = "gsavage"
        self.password = "GPassword2021"
        self.domain = "local"
        
        # self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ") 
        # self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):     
      return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

class ProtectedObjects(object):
    def protection_start_time(self, cohesity_client):
        time = cohesity_client.cluster.get_cluster()
        epoch = time.current_time_msecs
        standard_time = datetime.datetime.fromtimestamp(epoch/10**3)
        standard_time_delta = standard_time + datetime.timedelta(hours = -1)
        runs = []
        self.protection_runs = cohesity_client.protection_runs
        self.runs_list = self.protection_runs.get_protection_runs()
        for run in self.runs_list:
            run_time = datetime.datetime.fromtimestamp(run.backup_run.stats.start_time_usecs/10**6)
            if  run_time >= standard_time_delta:
                runs.append(run)
        return runs

  
  
def main():
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    protection_run = cc.protection_runs.get_protection_runs()
    protection_job = cc.protection_jobs.get_protection_jobs()
    # print(protection_run)
    # for run in protection_run:
    #     print(datetime.datetime.fromtimestamp(run.backup_run.stats.start_time_usecs/10**6))
    # time = cc.cluster.get_cluster()
    # print(time.current_time_msecs)

    protected_objects = ProtectedObjects()
    latest_run = protected_objects.protection_start_time(cc)

    #print(dir(latest_run))

    for run in latest_run:
        print(run.backup_run.stats.start_time_usecs)



#run main function
if __name__ == '__main__':
    main()
  