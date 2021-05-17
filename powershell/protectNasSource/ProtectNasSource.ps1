#This powershell script it to register genericNasSource
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN,
    
    [Parameter(Manadory =$True)]
    [ParameterType]
    $exportedFile
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
#$credSMB = Get-Credential -M "Please enter domain admin credentials with access to the SMB Shares"
#$ValidPath = Test-Path $NASList
try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh}
catch{Write-Output "Could not connect to the Cohesity Cluster.  Please make sure that the cluster FQDN or VIP is correct"}
#Testing
try{
    Get-CohesityProtectionSource -Environments KGenericNas
    Get-CohesityProtectionSource -Environments KGenericNas | export-csv GenericNasSources.csv -Delimiter ';'
}
catch{Write-Out "There was a problem importing Protection Sources"}
