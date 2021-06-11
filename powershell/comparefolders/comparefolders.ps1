#This powershell script is to compare two directories
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the source directory")]
    [String]
    $source, 
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster Port")]
    [String]
    $target
)
#$ErrorActionPreference = Continue;
$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("filehashcompare-" + $FileName + ".log")
try{
$sourceCompare = Get-ChildItem -Path $source -Recurse | Select-Object -Property *,
@{name="Hash";expression={(Get-FileHash $_.FullName -Algorithm MD5).hash}}
$targetCompare = Get-ChildItem -Path $target -Recurse | Select-Object -Property *,
@{name="Hash";expression={(Get-FileHash $_.FullName -Algorithm MD5).hash}}

}
catch{Write-warning $_.exception.message}
try{Compare-Object -ReferenceObject $sourceCompare -DifferenceObject $targetCompare -Property Name,Hash | Tee-Object -file $LogFile -Append}
catch{Write-warning $_.exception.message}
