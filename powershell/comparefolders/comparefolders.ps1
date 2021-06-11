#This powershell script is to compare two directories
param (
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the source directory")]
    [String]
    $source, 
    [Parameter(Mandatory=$True, HelpMessage = "Please enter the cluster Port")]
    [String]
    $target
)
try{
$sourceCompare = Get-ChildItem -Recurse -Path $source
$targetCompare = Get-ChildItem -Recurse -Path $target
}
catch{Write-warning $_.exception.message}

try{Compare-Object -ReferenceObject $sourceCompare -DifferenceObject $targetCompare}
catch{Write-warning $_.exception.message}