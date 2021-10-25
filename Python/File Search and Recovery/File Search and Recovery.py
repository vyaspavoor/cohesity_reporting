from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.exceptions.api_exception import APIException as api_exc
from cohesity_management_sdk.models.restore_files_task_request import RestoreFilesTaskRequest as restore_body
#rom cohesity_management_sdk.models.restored_file_info_list import RestoredFilesInfoList as recovered_file_info_list 

from cohesity_management_sdk.models.restored_file_info_list import RestoredFileInfoList as rere
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
        run_dict = {"start_time": self.protected_run[0].backup_run.stats.start_time_usecs,
                    "run_id":self.protected_run[0].backup_run.job_run_id }
        return run_dict
        
    
    
            
        #return dir(self.protected_run)
    
class ObjectsToRestore(object):
    def __init__(self, cohesity_client, search_text):
        self.restore_tasks = cohesity_client.restore_tasks
        
        #self.restore_taskss = cohesity_client.restore_tasks
        self.restore_search = self.restore_tasks.search_restored_files(search=search_text.casefold())
        #self.restore_body = self.restore_tasks.RestoreFilesTaskRequest()
        self.recovery_task_body = restore_body
        
    
    def recovery_file_search(self):
        for item in self.restore_search.files:
            return(item.job_id)
               
    def recover_file(self, job_id, job_run_id, run_start_time, cluster_id, incaarnation_id, source_id, target_id, environment):
        
        
        self.recovery_task_body.continue_on_error = True
        self.recovery_task_body.filenames = ["Vault1.txt"]
        self.recovery_task_body.filter_ip_config = False
        self.recovery_task_body.file_recovery_method = "kUseExistingAgent"
        self.recovery_task_body.is_file_based_volume_restore = True
        self.recovery_task_body.mount_disks_on_vm = False
        self.recovery_task_body.name = "Recovery_Task_test"
        self.recovery_task_body.new_base_directory = "/tmp/greg"
        self.recovery_task_body.overwrite = False
        # self.recovery_task_body.restored_file_info_list = []
        # self.recovery_task_body.restored_file_info_list.append(rere())
        # self.recovery_task_body.restored_file_info_list[0].is_directory = True
        self.recovery_task_body.restored_file_info_list = [{"isDirectory": True}]
        self.recovery_task_body.password = "Cohe$1ty"
        self.recovery_task_body.preserve_attributes = True
        self.recovery_task_body.source_object_info = {                                                             
        "environment": environment,
        "jobId": job_id,
        "jobRunId": job_run_id,
        "jobUid": {
            "clusterId": cluster_id,
            "clusterIncarnationId": incaarnation_id,
            "id": job_id
            },
        "protectionSourceId": source_id,
        "startedTimeUsecs": run_start_time
        },
        self.recovery_task_body.target_host_type = "kLinux"
        self.recovery_task_body.target_parent_source_id = 2,
        self.recovery_task_body.target_source_id = target_id,
        self.recovery_task_body.use_existing_agent = True,
        self.recovery_task_body.username = "cohesity"
        
        
        result = self.restore_tasks.create_restore_files_task(self.recovery_task_body)
        
        #self.create_restore_files_task(self.recovery_task_body)
        

    

def main():
    #Cohesity Authenticaiton
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    
    
    object_to_restore = ObjectsToRestore(cc, "vault1.txt")
    obj_restore = object_to_restore.recovery_file_search()
    
    cluster_config = ClusterConfig(cc)
    cluster_id = cluster_config.get_cluster_id()
    cluster_incarnation_id = cluster_config.get_cluster_incarnation_id()
    
    
    source_protected_source = ProtectedSources(cc, "10.26.0.81")
    source_id = source_protected_source.list_protected_source()
    target_protected_source = ProtectedSources(cc, "10.26.0.49")
    target_id = target_protected_source.list_protected_source()
    
    
    protected_group = ProtectedObjects(cc, "dtcc_test")
    protect_obj = protected_group.get_protected_jobs()
    run_obj = protected_group.get_protected_runs(protect_obj)
    
    
    run_id = run_obj['run_id']
    start_time = run_obj['start_time']
    print(source_id)
    recovery_obj = object_to_restore.recover_file(protect_obj, run_id , start_time, cluster_id, cluster_incarnation_id, source_id, target_id, "kPhysical") 
    
    #print(dir(exc))
if __name__ == '__main__':
    main()    
    