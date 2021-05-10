#This script is to get powershell permissions.
param (
    # Windows URL to path
    [Parameter(Mandatory)]
    [String]
    $dir
)
$ErrorActionPreference = "Continue";
try{
    $FileDate = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
    $FileName = New-Item -itemType File -Name ("UserNTFSPermissions_" + $FileDate + ".csv")
    Get-ChildItem -Path $dir | get-acl  | Format-Table -AutoSize -Property owner, path | export-csv $FileName
}
catch {Write-Output $_.exception.message}