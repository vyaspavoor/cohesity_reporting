#This powershell script it to delete paused protection jobs
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN,
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterPort,
    [Parameter(Mandatory=$True, HelpMessage="Please enter the CSV with teh list of NAS shares. Requires a hostname and path column")]
    [String]
    $NASList
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("setviewsmbsettings_" + $FileName + ".log")

try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh -port $ClusterPort}
catch{Write-warning $_.exception.message}

try{
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            $View = Get-CohesityView -ViewNames $_.Name
            $View.ProtocolAccess = 'KSMBonly'
            $View.EnableSmbViewDiscovery = $True
            try{Set-CohesityView -View $View | Tee-Object -File $LogFile -Append}
            catch{write-warning $_.exception.message}
        }
    }
}
catch{write-warning $_.exception.message}
  

Disconnect-CohesityCluster