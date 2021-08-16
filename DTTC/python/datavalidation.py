from cohesity_management_sdk.cohesity_client import CohesityClient
import getpass
import datetime
import os

class CohesityUserAuthentication(object):
    
    def __init__(self):
        """
        Intializing input authentication variables
        """
        self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ") 
        self.password = getpass.getpass(prompt='Please enter the user password: ', stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")
    #Authenticate to the cluster with credentials
    def user_auth(self):     
      return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

    def  return_cluster_ip(self):
        return self.cluster_ip
    
    def return_cluster_user(self):
        return self.username

    def return_cluster_domain(self):
        return self.domain

class ProtectedObjects(object):
    #Get the protection jobs that have run in the last hour
    def protection_start_time(self, cohesity_client):
        time = cohesity_client.cluster.get_cluster()
        epoch = time.current_time_msecs
        #Convert time in ms to standard time
        standard_time = datetime.datetime.fromtimestamp(epoch/10**3)
        standard_time_delta = standard_time + datetime.timedelta(hours = -1)
        runs = []
        self.protection_runs = cohesity_client.protection_runs
        self.runs_list = self.protection_runs.get_protection_runs()
        for run in self.runs_list:
            #Convert µsecs to standardtime
            run_time = datetime.datetime.fromtimestamp(run.backup_run.stats.start_time_usecs/10**6)
            if  run_time >= standard_time_delta:
                runs.append(run)
        return runs
    #Execute python script to get the files based upon the list of jobs that have run in the last hour
    def get_files_latest_runs(self, cohesity_client, cluster_ip, cluster_user, cluster_domain, protection_run_list):
        self.protection_jobs = cohesity_client.protection_jobs
        self.protection_sources = cohesity_client.protection_sources
        f = open("backupfilelog_"+ str(datetime.datetime.now()), "a")
        for run in protection_run_list:
            protection_job_obj = self.protection_jobs.get_protection_job_by_id(run.job_id)
            protection_job_name = protection_job_obj.name
            source_id = protection_job_obj.source_ids
            for id in source_id:
                source = cohesity_client.protection_sources.get_protection_sources_object_by_id(id)
                print(os.system("./backedUpFileList.py -v {cluster_ip} -u {cluster_user} -d {cluster_domain} \
                    -s {source_name} -j {job_name} -r {run_id}".format(cluster_ip=cluster_ip, cluster_user=cluster_user, \
                        cluster_domain=cluster_domain, source_name=source.name, job_name=protection_job_name, \
                             run_id=run.backup_run.job_run_id)), file=f)

  
def main():
    #User Authentication
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    
    #Cluster login artifact returns
    cluster_ip = cohesity_client.return_cluster_ip()
    cluster_user = cohesity_client.return_cluster_user()
    cluster_domain = cohesity_client.return_cluster_domain()
    
    #Protection runs
    protected_objects = ProtectedObjects()
    latest_run = protected_objects.protection_start_time(cc)
    
    #Files added to backup itteration
    backupfiles = protected_objects.get_files_latest_runs(cc, cluster_ip, cluster_user, cluster_domain, latest_run)


#run main function
if __name__ == '__main__':
    main()