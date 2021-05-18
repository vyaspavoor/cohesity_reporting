#This powershell script it to register genericNasSource
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster ID")]
    [String]
    $ClusterFQDN
    #[Parameter(Mandatory=$True, HelpMessage="Please enter the CSV with teh list of NAS shares. Requires a hostname and path column")]
    #[String]
    #$NASList
)
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
#$credSMB = Get-Credential -M "Please enter domain admin credentials with access to the SMB Shares"
#$ValidPath = Test-Path $NASList
try{Connect-CohesityCluster -Server $ClusterFQDN -Credential $credcoh}
catch{Write-warning "Could not connect to the Cohesity Cluster.  Please make sure that the cluster FQDN or VIP is correct"}

try{$sources = Get-CohesityProtectionSource -Environments KGenericNas}
catch{write-warning "unable to ubtain the generic nas protection sources"}
$sources | ForEach-Object{New-CohesityNASProtectionJob -name $_.protectionsource.name -SourceName $_.protectionsource.name -StorageDomainName DefaultStorageDomain -PolicyName Bronze -Confirm:$false}



