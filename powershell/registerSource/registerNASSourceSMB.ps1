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

try{
    #Connect-CohesityCluster -Server $ClusterFQDN -Credential (get-credential -t 'Please enter the Cluster')
    Import-CSV | ForEach-Object{
        $NASHostName = $_.'Hostname'
        $NASPath = $_.'Path'
        Write-Output $NASHostName + $nasPath
        #Register-CohesityProtectionSourceSMB
    }    
}
catch{}
Connect-CohesityCluster -Server 