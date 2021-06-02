#This powershell script it to delete paused protection jobs
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN,
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterPort
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("ProtectListNasSources_" + $FileName + ".log")
try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh -port $ClusterPort}
catch{Write-warning $_.exception.message}
try{$protectionjobs = Get-CohesityProtectionJob}
catch{write-warning $_.exception.message}
ForEach ($protectionjob in $protectionjobs){
    if($protectionjob.isPaused -eq $true)
        {
            Remove-CohesityProtectionJob -Name $protectionjob.name -KeepSnapshots -Confirm:$false | Tee-Object -File $LogFile -Append 
        
        }
}


Disconnect-CohesityCluster



