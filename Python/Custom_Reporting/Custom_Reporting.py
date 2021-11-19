from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.access_token_credential import AccessTokenCredential
from cohesity_management_sdk.exceptions.request_error_error_exception import RequestErrorErrorException
from cohesity_management_sdk.exceptions.api_exception import APIException
import datetime
import pandas as pd
import csv
import getpass

class CohesityUserAuthentication(object):
        
    
    def __init__(self, **kwargs):
        self.cohesity_client = kwargs.get('cohesity_client', CohesityUserAuthentication)
        #Intializing input authentication variables
        self.cluster_url = getpass._raw_input("Please enter the cluster VIP:  ")
        self.username = getpass._raw_input("Please Enter the username:  ")
        self.password = getpass.getpass(prompt="Please enter the user password: ", stream=None)
        self.domain = getpass._raw_input("Please Enter the user domain:  ")
        
        #Bearer Token Setup
        self.body = AccessTokenCredential()
        self.body.username = self.username
        self.body.password = self.password
        self.body.domain = self.domain

    #Authenticate to the cluster with credentials

    def user_auth(self):
        try:
            return CohesityClient(self.cluster_url, self.username, self.password, self.domain)
        except RequestErrorErrorException as e: 
            print(e)
        except APIException as e:
            print(e)
    
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

class CohesityProtectionJobObject(object):
    
    def __init__(self,  **kwargs):
        #Set optional parameters
        cohesity_client = kwargs.get('cohesity_client', CohesityClient)
        
        #Declare protection jobs object
        self.protection_jobs = cohesity_client.protection_jobs
        try:
            self.protection_job_objects = self.protection_jobs.get_protection_jobs()
        except RequestErrorErrorException as e: 
            print(e)
        except APIException as e:
            print(e)
        
        #Create policy variables and objects
        self.protection_policies = cohesity_client.protection_policies
        
        #Create source object
        self.protection_sources = cohesity_client.protection_sources
        
         #Create job run object
        self.protection_runs = cohesity_client.protection_runs
        
        #Create cluster object
        self.cohesity_cluster = cohesity_client.cluster
        try:
            self.cluster = self.cohesity_cluster.get_cluster()
        except RequestErrorErrorException as e: 
            print(e)
        except APIException as e:
            print(e)
        
        #Setup report naming
        self.cluster_name = self.cluster.name
        self.cluster_time = datetime.datetime.fromtimestamp(self.cluster.current_time_msecs/10**3).strftime('%H%M%S_%m%d%Y')
        self.report_name = self.cluster_name + '_' + self.cluster_time +'_Backupreport.csv'
        
        #Declare empty dictionary
        self.job_dict = {}
        
        #Declare job_name list
        self.job_names = []
        
    def create_job_dictionary(self):
        for job in self.protection_job_objects:
            if '_deleted_'.upper() not in job.name:
                self.job_dict[job.name] = {}
                self.job_dict[job.name]["Job Id"] = job.id
                self.job_dict[job.name]["Job Name"] = job.name
                self.job_dict[job.name]["Source Id"] = job.source_ids
                self.job_dict[job.name]["Policy Id"] = job.policy_id
                self.job_dict[job.name]["Environment"] = job.environment
                self.job_dict[job.name]["Description"] = job.description         
        return self.job_dict
    
    def create_job_name_list(self, job_dictionary):
        for name in self.job_dict.keys():
            self.job_names.append(name)
        return self.job_names
        
    def append_policy_name_dictionary(self, appended_job_dict, job_name_list):
        count = 0
        #iterate through policy object and set attributes
        self.appended_job_dict = appended_job_dict
        for name in job_name_list:
            if  self.protection_policies.get_protection_policies != None:
                try:
                    protection_policy_objects = self.protection_policies.get_protection_policy_by_id(id = self.job_dict[name]["Policy Id"])
                except RequestErrorErrorException as e: 
                    continue
                except APIException as e:
                    continue
                #Obtain Policy information    
                self.appended_job_dict[name]["Policy Name"] = protection_policy_objects.name
                self.appended_job_dict[name]["Days to Keep"] = protection_policy_objects.days_to_keep
                if protection_policy_objects.extended_retention_policies != None:
                    self.appended_job_dict[name]["Extended Retention"] =  protection_policy_objects.extended_retention_policies[0].days_to_keep
                else:
                   self.appended_job_dict[name]["Extended Retention"] = "No extended retention"
            else:
               self.appended_job_dict[name]["Policy Name"] = "Policy Deleted"
               self.appended_job_dict[name]["Days to Keep"] = "Retention not found"         
        return self.appended_job_dict
   
    def append_source_name_dictionary(self, appended_job_dict, job_names_list):
        self.appended_job_dict = appended_job_dict
        for name in job_names_list:
            #Create name list for use later
            source_names = []
            #Iterate through the List nested in the dictionary
            for id in self.appended_job_dict[name]["Source Id"]:
                try:
                    source = self.protection_sources.list_protection_sources(id=id)
                except RequestErrorErrorException as e: 
                    continue
                except APIException as e:
                    continue
                source_names.append(source[0].protection_source.name)
            self.appended_job_dict[name]["Source Name"] = source_names
        return self.appended_job_dict
                       
    def append_latest_protection_run_dictionary(self, appended_job_dict, job_names_list):
        self.appended_job_dict = appended_job_dict
        
        for name in job_names_list:
            runs = []
            try:
                job_runs = self.protection_runs.get_protection_runs(job_id = self.appended_job_dict[name]["Job Id"], num_runs= 2)
            except RequestErrorErrorException as e: 
                continue
            except APIException as e:
                continue
            #iterate through jobs and set attributes
            for job in job_runs:
                if self.appended_job_dict[name]["Job Id"] == job.job_id:
                    runs.append(job) 
                    self.appended_job_dict[name]["Snapshot Deleted"] = runs[0].backup_run.snapshots_deleted
                    self.appended_job_dict[name]["Job Start Time"] = datetime.datetime.fromtimestamp(runs[0].backup_run.stats.start_time_usecs/10**6).strftime('%m-%d-%Y %H:%M:%S')
                    self.appended_job_dict[name]["Job End Time"] = datetime.datetime.fromtimestamp(runs[0].backup_run.stats.end_time_usecs/10**6).strftime('%m-%d-%Y %H:%M:%S')
                    self.appended_job_dict[name]["Total Bytes Read"] = runs[0].backup_run.stats.total_bytes_read_from_source
                    self.appended_job_dict[name]["Total Logical Backup Size"] = runs[0].backup_run.stats.total_logical_backup_size_bytes
                    if runs[0].copy_run[0].target.replication_target != None:
                        self.appended_job_dict[name]["Replication Target"] = runs[0].copy_run[0].target.replication_target.cluster_name
                    else:
                        self.appended_job_dict[name]["Replication Target"] = "No Replicatoin Cluster"
                    self.appended_job_dict[name]["Latest Backup Run Status"] = runs[0].backup_run.status
                    
                    if len(runs) >= 2:
                        self.appended_job_dict[name]["Previous Backup Status"] = runs[1].backup_run.status
                    else:
                        self.appended_job_dict[name]["Previous Backup Status"] = "No Previous Run Found"       
        return self.appended_job_dict
                
    def clean_appended_dict(self, appended_job_dict, job_names_list):
        self.appended_job_dict = appended_job_dict
        #Iterate through dictionary and remove 
        for name in job_names_list:
            self.appended_job_dict[name].pop("Policy Id")
            self.appended_job_dict[name].pop("Source Id")
            self.appended_job_dict[name].pop("Job Id")
        return self.appended_job_dict
    
    def save_as_csv(self, appended_job_dict, job_names_list):
        self.appended_job_dict = appended_job_dict
        #Setup the dataframe for export to CSV
        df = pd.DataFrame(self.appended_job_dict).rename_axis('job name').reset_index().transpose()
        #Iterate and add dictionaries as rows and columns
        for name in job_names_list:
            df = df.rename(columns=appended_job_dict[name])
        #export to csv
        df.to_csv(self.report_name, index=False)

def main():
    #SDK Authenticaation to the cluster
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    #Protection Job  Object
    protection_job_object = CohesityProtectionJobObject(cohesity_client = cc)
    #Protection Job Dictionary
    protection_job_dictionary = protection_job_object.create_job_dictionary()
    #Add job names
    cohesity_protection_jobs_names = protection_job_object.create_job_name_list(protection_job_dictionary)
    #Add policy names
    cohesity_protection_policy_names = protection_job_object.append_policy_name_dictionary(protection_job_dictionary, cohesity_protection_jobs_names)
    #Add protection source names
    cohesity_protection_source_names = protection_job_object.append_source_name_dictionary(cohesity_protection_policy_names, cohesity_protection_jobs_names)
    #Add protection runs and previous run state
    cohesity_protection_run_info = protection_job_object.append_latest_protection_run_dictionary(cohesity_protection_source_names, cohesity_protection_jobs_names)
    #Clean dictionary of Ids
    cohesity_cleaned_dictionary = protection_job_object.clean_appended_dict(cohesity_protection_run_info, cohesity_protection_jobs_names)
    #Create csv
    create_csv = protection_job_object.save_as_csv(cohesity_cleaned_dictionary, cohesity_protection_jobs_names)
if __name__ == '__main__':
    main()
        