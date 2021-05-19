#This powershell script it to register genericNasSource
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN, 
    [Parameter(Mandatory=$True, HelpMessage="Please enter the CSV with teh list of NAS shares. Requires a hostname and path column")]
    [String]
    $NASList
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$credSMB = Get-Credential -M "Please enter domain admin credentials with access to the SMB Shares"
$ValidPath = Test-Path $NASList -PathType Any
try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh}
catch{
    Write-warning "Could not connect to the Cohesity Cluster.  Please make sure that the cluster FQDN or VIP is correct"
    Write-warning $_.exception.message
        }

try{  
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            $NASHostName = $_.Hostname
            $NASPath = $_.Path
            $Path = '\\'+ $NasHostName + '\' + $NASPath
            try{Register-CohesityProtectionSourceSMB -MountPath $Path -Credential $credSMB}
            catch{Write-warning $_.exception.message}
        }
    }
    else {
        Write-warning "The file $NASList is not a valid file"
    }    
}
catch{Write-warning $_.exception.message}
Disconnect-CohesityCluster

