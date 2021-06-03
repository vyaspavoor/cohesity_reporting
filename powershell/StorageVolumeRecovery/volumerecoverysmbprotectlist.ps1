#This powershell script it to register genericNasSource
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
#Variable Setup
$ErrorActionPreference = "Stop";
$credcoh = Get-Credential -Message "Enter the Cohesity cluster credentials. "
$ValidPath = Test-Path $NASList -PathType Any
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("ListStorageVolumeRecovery-" + $FileName + ".log")
#Connect to Cluster
try{Connect-CohesityCluster -Server $ClusterFQDN -Port $ClusterPort -Credential $credcoh}
catch{    Write-warning $_.exception.message}
#Storage Volume Recovery
try{  
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            try{Restore-CohesityBackupToView -TargetViewName $_.Name -QOSPolicy 'TestAndDev High' -ProtectionJobName $_.Hostname | Tee-Object -file $LogFile -Append}
            catch{Write-warning $_.exception.message}
           
        }
    }
    else {
        Write-warning "The file $NASList is not a valid file"
    }    
}
catch{Write-warning $_.exception.message}
#Setting Protocol to SMB Only and making SMB browseable
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
#Protection Job Creation
try{  
    if ($ValidPath -eq $True){
        Import-CSV $NASList | ForEach-Object{
            $View = Get-CohesityView -ViewNames $_.Name
            $sourceviewid = $View.ViewId
            
            #try{New-CohesityProtectionJob -name $_.Name -StorageDomainName $storageDomain -PolicyName $protectionPolicy -TimeZone 'America/Los_Angeles' -ViewName $_.Name -Environment kView | Tee-Object -file $LogFile -Append}
            #catch{Write-warning $_.exception.message}
        } 
    }
    else {
        Write-warning "The file $NASList is not a valid file"  
    }    
}
catch{Write-warning $_.exception.message}

Disconnect-CohesityCluster
