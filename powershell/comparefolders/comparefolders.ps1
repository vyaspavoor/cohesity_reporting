#This powershell script is to compare two directories
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the source directory")]
    [String]
    $source, 
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster Port")]
    [String]
    $target
)

$FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
$LogFile = New-Item -itemType File -Name ("filehashcompare-" + $FileName + ".log")
try{
$sourceCompare = Get-ChildItem -Path $source -Recurse | Get-FileHash -Algorithm md5
$targetCompare = Get-ChildItem -Path $target -Recurse  | Get-FileHash -Algorithm md5
}
catch{Write-warning $_.exception.message}
try{Compare-Object -ReferenceObject $sourceCompare -DifferenceObject $targetCompare | Tee-Object -file $LogFile -Append}
catch{Write-warning $_.exception.message}