from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.access_token_credential import AccessTokenCredential
from cohesity_management_sdk.exceptions.request_error_error_exception import RequestErrorErrorException
from cohesity_management_sdk.exceptions.api_exception import APIException


class CohesityUserAuthentication(object):
        
    
    def __init__(self, **kwargs):
        self.cohesity_client = kwargs.get('cohesity_client', CohesityUserAuthentication)
        #Intializing input authentication variables
        # self.cluster_ip = getpass._raw_input("Please enter the cluster VIP:  ")
        # self.username = getpass._raw_input("Please Enter the username:  ")
        # self.password = getpass.getpass(prompt="Please enter the user password: ", stream=None)
        # self.domain = getpass._raw_input("Please Enter the user domain:  ")
        
        self.cluster_url = "10.26.0.159"
        self.username = "gsavage"
        self.password = "GPassword2021"
        self.domain = "local"
        
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
            print("There was an excepiton with the JSON Payload")
        except APIException as e:
            print("There was a problem with the your credentials  Please try again", e)
    
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
            print("There was a problem with the payload")
        except APIException as e:
            print("There was a problem with the API request")
        
        #Create policy variables and objects
        self.protection_policies = cohesity_client.protection_policies
        
        #Create source object
        self.protection_sources = cohesity_client.protection_sources
        
         #Create job run object
        self.protection_runs = cohesity_client.protection_runs
        
        #Declare empty dictionary
        self.job_dict = {}
        
        #Declare job_name list
        self.job_names = []
        
    
    def create_job_dictionary(self):
        for job in self.protection_job_objects:
            if '_deleted_'.upper() not in job.name:
                self.job_dict[job.name] = {}
                self.job_dict[job.name]["Job Id"] = job.id
                self.job_dict[job.name]["Source Id"] = job.source_ids
                self.job_dict[job.name]["Policy Id"] = job.policy_id
                self.job_dict[job.name]["Description"] = job.description
        return self.job_dict
    
    def create_job_name_list(self, job_dictionary):
        for name in self.job_dict.keys():
            self.job_names.append(name)
        return self.job_names
        
    def append_policy_name_dictionary(self, appended_job_dict, job_name_list):
        count = 0
        #self.protection_policy_objects = self.protection_policies.get_protection_policies()
        self.appended_job_dict = appended_job_dict
        for name in job_name_list:
    
            try:
                protection_policy_objects = self.protection_policies.get_protection_policy_by_id(id = self.job_dict[name]["Policy Id"])
            except RequestErrorErrorException as e: 
                continue
            except APIException as e:
                continue    
            self.appended_job_dict[name]["Policy Name"] = protection_policy_objects.name
        return self.appended_job_dict
   
            

    def append_source_name_dictionary(self, appended_job_dict, job_names_list):
        self.appended_job_dict = appended_job_dict
        for name in job_names_list:
            #Create name list for use later
            source_names = []
            #Itterate through the List nested in the dictionary
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
            run_id = []
            try:
                job_run = self.protection_runs.get_protection_runs(job_id = self.appended_job_dict[name]["Job Id"], num_runs= 2)
            except RequestErrorErrorException as e: 
                continue
            except APIException as e:
                continue
            
            for job in job_run:
                
                # print(self.appended_job_dict[name])
                if self.appended_job_dict[name]["Job Id"] == job.job_id:
                    run_id.append(job.backup_run.job_run_id)
                self.appended_job_dict[name]["Run Ids"] = run_id
        return self.appended_job_dict
    
    
            
            # print(run_id)
                # print(job.job_name, job.backup_run.job_run_id)
            # for job_id in self.appended_job_dict[name]["Job Id"]:
                # try:
                #     job_run = self.protection_runs.get_protection_runs(job_id = job_id["Job Id"])
                # except RequestErrorErrorException as e: 
                #     continue
                # except APIException as e:
                #     continue
            # print(job_run.backup_run.start_time_usecs)
            # print(self.appended_job_dict[name]["Job Id"])
                #print(job_id[name])
        
    

def main():
    #SDK Authenticaation to the cluster
    cohesity_client = CohesityUserAuthentication()
    cc = cohesity_client.user_auth()
    #print(type(cc))
    
    #Protection Job Dictionary
    protection_job_object = CohesityProtectionJobObject(cohesity_client = cc)
    protection_job_dictionary = protection_job_object.create_job_dictionary()
    cohesity_protection_jobs_names = protection_job_object.create_job_name_list(protection_job_dictionary)
    cohesity_protection_policy_names = protection_job_object.append_policy_name_dictionary(protection_job_dictionary, cohesity_protection_jobs_names)
    cohesity_protection_source_names = protection_job_object.append_source_name_dictionary(cohesity_protection_policy_names, cohesity_protection_jobs_names)
    cohesity_protection_run_info = protection_job_object.append_latest_protection_run_dictionary(cohesity_protection_source_names, cohesity_protection_jobs_names)
    #print(cohesity_protection_source_names)
    
    
    
if __name__ == '__main__':
    main()
        