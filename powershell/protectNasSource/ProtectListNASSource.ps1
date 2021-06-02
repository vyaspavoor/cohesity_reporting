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
    $NASList,
    [Parameter(Mandatory=$True, HelpMessage="Please enter the target Storage Domain")]
    [String]
    $storageDomain,
    [Parameter(Mandatory=$True, HelpMessage="Please enter the protection policy name")]
    [String]
    $protectionPolicy
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$ValidPath = Test-Path $NASList -PathType Any
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("ProtectionListNASSource-" + $FileName + ".log")
try{Connect-CohesityCluster -Server $ClusterFQDN -Port $ClusterPort -Credential $credcoh}
catch{    Write-warning $_.exception.message}

try{  
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            $NASHostName = $_.Hostname
            $NASPath = $_.Name
            $NasName = $NasHostName + '\' + $NASPath
            $Path = '\\'+ $NasName
            $JobName = $NasName.replace('\', '-') 
            try{New-CohesityNASProtectionJob -name $JobName -SourceName $Path -StorageDomainName $storageDomain -PolicyName $protectionPolicy -TimeZone 'America/Los_Angeles'  -Confirm:$false | Tee-Object -file $LogFile -Append}
            catch{Write-warning $_.exception.message}
        }
    }
    else {
        Write-warning "The file $NASList is not a valid file"
    }    
}
catch{Write-warning $_.exception.message}
Disconnect-CohesityCluster

