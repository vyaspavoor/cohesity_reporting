#This powershell script it to register protect a generic nas
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN, 
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster Port")]
    [String]
    $ClusterPort,
    [Parameter(Mandatory=$True, HelpMessage="Please enter the CSV with teh list of NAS shares. Requires a hostname and path column")]
    [String]
    $NASList
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$ValidPath = Test-Path $NASList -PathType Any
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("ProtectionRunListNASSource-" + $FileName + ".log")
try{Connect-CohesityCluster -Server $ClusterFQDN -Port $ClusterPort -Credential $credcoh}
catch{    Write-warning $_.exception.message}

try{  
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            try{Start-CohesityProtectionJob -Name $_.Name | Tee-Object -file $LogFile -Append}
            catch{Write-warning $_.exception.message}
        }
    }
    else {
        Write-warning "The file $NASList is not a valid file"
    }    
}
catch{Write-warning $_.exception.message}
Disconnect-CohesityCluster


