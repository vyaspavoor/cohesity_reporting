#This powershell script it to register genericNasSource
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh}
catch{Write-Output "Could not connect to the Cohesity Cluster.  Please make sure that the cluster FQDN or VIP is correct"}
try{
    Get-CohesityProtectionSource -Environments KGenericNas
    Get-CohesityProtectionSource -Environments KGenericNas | export-csv GenericNasSources.csv -Delimiter ';'
}
catch{Write-Out "There was a problem exporting NAS Protection Sources"}
