#This powershell script it to register genericNasSource
[CmdletBinding()]
param (
    [Parameter(Mandatory)]
    [String]
    $ClusterFQDN, 
    [Parameter(Mandatory)]
    [String]
    $NASList
)
$ErrorActionPreference = "Stop";
try{
    $cred = Get-Credential -Message "enter this"
    Connect-CohesityCluster -Server $ClusterFQDN -Credential $cred
}
catch{Write-Output "Could not connect to the Cohesity Cluster.  Please make sure that the cluster FQDN or VIP is correct"}
$ValidPath = Test-Path $NASList
try{  
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            $NASHostName = $_.'Hostname'
            $NASPath = $_.'Path'
            $Path ='\\'+ $NasHostName + '\' + $NASHostName
            Write-Output $Path
    #Register-CohesityProtectionSourceSMB
        }
    }
    else {
        Write-Output "The file $NASList is not a valid file"
    }    
}
catch{}
