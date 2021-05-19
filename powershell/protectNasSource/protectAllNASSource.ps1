#This powershell script it to register genericNasSource
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN,
    [Parameter(Mandatory=$True, HelpMessage="Please enter the target Storage Domain")]
    [String]
    $storageDomain,
    [Parameter(Mandatory=$True, HelpMessage="Please enter the protection policy name")]
    [String]
    $protectionPolicy
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("ProtectListNasSources_" + $FileName + ".log")
try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh}
catch{Write-warning $_.exception.message}

try{$sources = Get-CohesityProtectionSource -Environments KGenericNas}
catch{write-warning $_.exception.message}
try{$sources | ForEach-Object{New-CohesityNASProtectionJob -name $_.protectionsource.name -SourceName $_.protectionsource.name -StorageDomainName $storageDomain -PolicyName $protectionPolicy -Confirm:$false | Tee-Object -file $LogFile -Append}}
catch{write-warning $_.exception.message}
Disconnect-CohesityCluster



