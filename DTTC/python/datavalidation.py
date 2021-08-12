from cohesity_management_sdk.cohesity_client import CohesityClient
import getpass
import datetime
import os

class CohesityUserAuthentication(object):
    
    def __init__(self):
        """
        Intializing input authentication variables
        """
        # self.cluster_ip = "10.26.0.159"
        # self.username = "gsavage"
        # self.password = "GPassword2021"
        # self.domain = "local"
        
        self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ") 
        self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")

    def user_auth(self):     
      return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

    def  return_cluster_ip(self):
        return self.cluster_ip

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
    cluster_ip = cohesity_client.return_cluster_ip()
    protection_run = cc.protection_runs.get_protection_runs()
    protection_job = cc.protection_jobs.get_protection_jobs()

    protected_objects = ProtectedObjects()
    latest_run = protected_objects.protection_start_time(cc)


    for run in latest_run:
        protection_job = cc.protection_jobs.get_protection_job_by_id(run.job_id)
        protection_job_name = protection_job.name
        source_id = protection_job.source_ids
        #print(dir(source_id))
        for id in source_id:
            # print(id)
            source = cc.protection_sources.get_protection_sources_object_by_id(id)
            #print("The proetectoin source name is {source_name} the protection job name is {job_name} and the protection run id is {run_id}".format(source_name=source.name, job_name=protection_job_name, run_id=run.backup_run.job_run_id))
            print(os.system("./backedUpFileList.py -v {cluster_ip} -u gsavage -d local -s {source_name} -j {job_name} -r {run_id}".format(cluster_ip=cluster_ip, source_name=source.name, job_name=protection_job_name, run_id=run.backup_run.job_run_id)))


#run main function
if __name__ == '__main__':
    main()