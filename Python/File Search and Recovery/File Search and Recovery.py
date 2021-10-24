from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.exceptions.api_exception import APIException as api_exc
from cohesity_management_sdk.models.restore_files_task_request import RestoreFilesTaskRequest as body
import datetime
import getpass
import os

class api_except(api_exc):
    pass

class CohesityUserAuthentication(object):
        
    
    def __init__(self):
        #Intializing input authentication variables

        # self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ")
        # self.password = getpass.getpass(prompt="Please enter the user password: ", stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")
        self.cluster_ip = "10.26.14.231"
        self.username = "admin"
        self.password = "Cohe$1ty"
        self.domain = "local"

    #Authenticate to the cluster with credentials

    def user_auth(self):
        return CohesityClient(self.cluster_ip, self.username, self.password, self.domain)

            

    def return_cluster_ip(self):
        return self.cluster_ip

    def return_cluster_user(self):
        return self.username
    def return_cluster_domain(self):
        return self.domain

class ClusterConfig(object):
    def __init__(self, cohesity_client):
        self.cluster = cohesity_client.cluster
        self.cluster_info = self.cluster.get_cluster()
    
    def get_cluster_id(self):
       return self.cluster_info.id
   
    def get_cluster_incarnation_id(self):
        return self.cluster_info.incarnation_id
    
class ProtectedSources(object):
    def __init__(self, cohesity_client, name):
        self.protection_sources = cohesity_client.protection_sources
        self.list_protection_sources = self.protection_sources.list_protection_sources()
        self.name = name
        self.source_list = []
        
    def list_protected_source(self):
        for source in self.list_protection_sources:
            #return source
            for node in source.nodes:
                if node['protectionSource']['name'] == self.name:
                    return node['protectionSource']['id']
       
             
    
class ProtectedObjects(object):
    def __init__(self, cohesity_client, job_name):
        #Init Protection Jobs
        self.protection_jobs = cohesity_client.protection_jobs
        self.protected_group = self.protection_jobs.get_protection_jobs(names=job_name)
        
        #Init Protection Runs
        self.protection_runs = cohesity_client.protection_runs
       
        
    def get_protected_jobs(self):
        return self.protected_group[0].id
        #return type(self.protected_group)
        
    def get_protected_runs(self, job_id):
        self.protected_run = self.protection_runs.get_protection_runs(job_id)
        return self.protected_run[0].backup_run.stats.start_time_usecs
            
        #return dir(self.protected_run)
    
class ObjectsToRestore(object):
    def __init__(self, cohesity_client, search_text):
        self.restore_tasks = cohesity_client.restore_tasks
        self.restore_search = self.restore_tasks.search_restored_files(search=search_text.casefold())
    
    def recovery_file_search(self):
        for item in self.restore_search.files:
            return(item.job_id)
               
    def recover_file(self, job_id, job_run_id, run_start_time, cluster_id, incaarnation_id, source_id, target_id, environment):
        recovery_task_body = body
        body.name = "Recovery_Task_test"
        body.sourceObjectInfo = {
        "environment": "kPhysical",
        "jobId" : 31,
        "jobRunId": 2148,
        "jobUid": {
            "clusterId": 1089765256393000,
            "clusterIncarnationId": 1633708596754,
            "id": 31
        },
        "protectionSourceId": 7,
        "startedTimeUsecs": 1634235153603583
    }
        

        #result = restore_tasks_controller.create_restore_files_task(body)
    

def main():
    #Cohesity Authenticaiton
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    
    
    object_to_restore = ObjectsToRestore(cc, "vault4.txt")
    obj_restore = object_to_restore.recovery_file_search()
    
    cluster_config = ClusterConfig(cc)
    cluster_id = cluster_config.get_cluster_id()
    cluster_incarnation_id = cluster_config.get_cluster_incarnation_id()
    
    
    source_protected_source = ProtectedSources(cc, "10.26.1.87")
    source_id = source_protected_source.list_protected_source()
    target_protected_source = ProtectedSources(cc, "10.26.1.149")
    
    
    protected_group = ProtectedObjects(cc, "murph-ransomware-test")
    protect_obj = protected_group.get_protected_jobs()
    run_obj = protected_group.get_protected_runs(protect_obj)
    
    
    #print(dir(exc))
if __name__ == '__main__':
    main()    
    