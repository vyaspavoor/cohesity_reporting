from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.exceptions.api_exception import APIException as api_exc
from cohesity_management_sdk.models.restore_files_task_request import RestoreFilesTaskRequest as restore_body
from cohesity_management_sdk.models.restore_object_details import RestoreObjectDetails as rod
from cohesity_management_sdk.models.restored_file_info_list import RestoredFileInfoList as rfil
from cohesity_management_sdk.models.universal_id import UniversalId as uid
from cohesity_management_sdk.models.target_host_type_enum import TargetHostTypeEnum as TargetHostTypeEnum
from cohesity_management_sdk.models.access_token_credential import AccessTokenCredential 
from cohesity_management_sdk.models.access_token import AccessToken
import getpass
import os
import requests
import json
import datetime
class api_except(api_exc):
    pass

class CohesityUserAuthentication(object):
        
    
    def __init__(self, **kwargs):
        self.cohesity_client = kwargs.get('cohesity_client', CohesityUserAuthentication)
        #Intializing input authentication variables
        # self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ")
        # self.password = getpass.getpass(prompt="Please enter the user password: ", stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")
        
        self.cluster_url = "10.26.14.231"
        self.username = "admin"
        self.password = "Cohe$1ty"
        self.domain = "local"
        
        #Bearer Token Setup
        self.body = AccessTokenCredential()
        self.body.username = self.username
        self.body.password = self.password
        self.body.domain = self.domain

    #Authenticate to the cluster with credentials

    def user_auth(self):
        return CohesityClient(self.cluster_url, self.username, self.password, self.domain)
    
    def get_bearer_token(self):
        self.access_token = self.cohesity_client.access_tokens
        bearer_token = self.access_token.create_generate_access_token(self.body)
        return bearer_token


    def get_cluster_url(self):
        return self.cluster_url

    def get_cluster_user(self):
        return self.username
    def get_cluster_domain(self):
        return self.domain
    

class ClusterConfig(object):
    def __init__(self, cohesity_client):
        self.cluster = cohesity_client.cluster
        self.cluster_info = self.cluster.get_cluster()
    
    def get_cluster_id(self):
       return self.cluster_info.id
   
    def get_cluster_incarnation_id(self):
        return self.cluster_info.incarnation_id
    
    def system_time(self):
        current_time = self.cluster_info.current_time_msecs
        return datetime.datetime.fromtimestamp(current_time/10**3)
    
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
    def __init__(self, cohesity_client, job_name, **kargs):
        #Init Protection Jobs
        self.protection_jobs = cohesity_client.protection_jobs
        self.protected_group = self.protection_jobs.get_protection_jobs(names=job_name)
        
        #Init Protection Runs
        self.protection_runs = cohesity_client.protection_runs
       
        
    def get_protected_jobs(self):
        return self.protected_group[0]
        #return type(self.protected_group)
   
    def get_protected_runs(self, job_id):
        
        self.protected_run = self.protection_runs.get_protection_runs(job_id)
        run_dict = {"start_time": self.protected_run[0].backup_run.stats.start_time_usecs,
                    "run_id":self.protected_run[0].backup_run.job_run_id }
        return run_dict
        
    
    
            
        #return dir(self.protected_run)
    
class ObjectsToRestore(object):
    def __init__(self, cohesity_client, search_text):
        self.host_type = TargetHostTypeEnum.KLINUX
        self.restore_tasks = cohesity_client.restore_tasks
        
        #self.restore_taskss = cohesity_client.restore_tasks
        self.restore_search = self.restore_tasks.search_restored_files(search=search_text.casefold())
        #self.restore_body = self.restore_tasks.RestoreFilesTaskRequest()
        self.recovery_task_body = restore_body
        
    
    def recovery_file_search(self):
        for item in self.restore_search.files:
            return item.filename    
    
    def recover_file(self, **kwargs):
        bearer_token = kwargs.get('bearer_token', AccessToken)
        cluster_current_time = kwargs.get('cluster_current_time', datetime.datetime)
        cluster_id = kwargs.get('cluster_id', int)
        cluster_incarnation_id = kwargs.get('cluster_incarnation_id', int)
        cluster_url = kwargs.get('cluster_url', str)
        environment = kwargs.get('environment', str)
        file_name = kwargs.get('file_name', str)
        job_id = kwargs.get('job_id', int)
        job_name =kwargs.get('job_name', str)
        job_run_id = kwargs.get('job_run_id', int)
        job_run_start_time = kwargs.get('job_run_start_time', int)
        source_id = kwargs.get('source_id', int)
        target_id = kwargs.get('target_id', int)
        
          
        recovery_name =  "Recovery"+job_name+str(cluster_current_time)
        headers = {"Authorization": "Bearer %s" % bearer_token.access_token}
        #REST API Url
        url = 'https://{cluster_url}/irisservices/api/v1/public/restore/files'.format(cluster_url=cluster_url)
                
        payload = {
                "continueOnError": False,
                "filenames": [
                    file_name
                ],
                "isFileBasedVolumeRestore": True,
                "name": recovery_name,
                "newBaseDirectory": "/tmp/test/",
                "overwrite": True,
                "password": "Cohe$1ty",
                "preserveAttributes": True,
                "sourceObjectInfo": {
                    "environment": environment,
                    "jobId": job_id,
                    "jobRunId": job_run_id,
                    "jobUid": {
                        "clusterId": cluster_id,
                        "clusterIncarnationId": cluster_incarnation_id,
                        "id": job_id
                    },
                    "protectionSourceId": source_id,
                    "startedTimeUsecs": job_run_start_time
                },
                "targetParentSourceId": 2,
                "targetSourceId": target_id,
                "useExistingAgent": True,
                "username": "cohesity"
        }
        # print(file_name)
        req = requests.post(url=url, data=json.dumps(payload), headers=headers, verify=False)
        print("The protection_group {job_name} has been recovered".format(job_name=job_name))
        

    

def main():
    #Cohesity Authenticaiton
    search_string = '/home/cohesity/vault1'
    protection_source = '10.26.0.81'
    recovery_target = '10.26.0.49'
    protection_group = 'dtcc_test'
    environment = 'kPhysical'
    
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    bearer_client = CohesityUserAuthentication(cohesity_client=cc)
    bearer_token = bearer_client.get_bearer_token()
    cluster_url = cohesity_client.get_cluster_url()
     
    object_to_restore = ObjectsToRestore(cc, search_string)
    file_name = object_to_restore.recovery_file_search()
    
    cluster_config = ClusterConfig(cc)
    cluster_id = cluster_config.get_cluster_id()
    cluster_incarnation_id = cluster_config.get_cluster_incarnation_id()
    cluster_current_time = cluster_config.system_time()
    
    
    source_protected_source = ProtectedSources(cc, protection_source)
    source_id = source_protected_source.list_protected_source()
    target_protected_source = ProtectedSources(cc, recovery_target)
    target_id = target_protected_source.list_protected_source()
    
    
    protected_group = ProtectedObjects(cc, protection_group)
    protect_obj = protected_group.get_protected_jobs()
    run_obj = protected_group.get_protected_runs(protect_obj.id)
    #print(file_name)
    
    job_id = protect_obj.id
    job_name = protect_obj.name
    
    job_run_id = run_obj['run_id']
    job_run_start_time = run_obj['start_time']
    
    recovery_obj = object_to_restore.recover_file(bearer_token=bearer_token, job_name=job_name, job_id=job_id, job_run_id=job_run_id, \
        job_run_start_time=job_run_start_time, cluster_id=cluster_id, cluster_incarnation_id=cluster_incarnation_id, \
            source_id=source_id, target_id=target_id, environment=environment, cluster_url=cluster_url, \
                cluster_current_time=cluster_current_time, file_name=file_name) 
    
    # print(job_name)
if __name__ == '__main__':
    main()    
    