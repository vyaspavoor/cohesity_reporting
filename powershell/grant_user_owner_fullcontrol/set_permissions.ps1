#This scirpt is designed to change permissions on folders that have permission denied.  Requries a domain/enterprise admin account with the ability to take ownership of files.
param (
# Input CSV file
[Parameter(Mandatory)]
[String]
$csv,

# Username Input
[Parameter(Mandatory)] 
[String]
$AdminUser,

# Hostname
#[Parameter(Mandatory)]UserNTFSPermissions_08-05-2021-10-18-47.csv
#[String]
#$HostName,

# Share hame
[Parameter(Mandatory)]
[String]
$dir
)
$ErrorActionPreference = "Continue";
try {
    $FileDate = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
    $LogFile = New-Item -itemType File -Name ("PermissionChangeLog_" + $FileDate + ".txt")
    Import-Csv $csv | ForEach-Object{
        #Ownership and Permission Change
        #$OriginalPath = $_.'Path'
        
        #$Path = Convert-Path $OriginalPath
        #out-file $Path
        #$Path = "\\" + $HostName + '\' + $Share + $NewPath
        $ValidPath = Test-Path $Path 
        if ($ValidPath -eq $True){
            $acl = get-acl -path $Path 
            $user = New-Object  System.Security.Principal.NTAccount($AdminUser)
            $acl.SetOwner($user)
            $access_rule = New-Object System.Security.AccessControl.FileSystemAccessRule($AdminUser,"FullControl","Allow")
            $acl.SetAccessRule($access_rule)
            set-acl -path $Path -aclobject $acl
            Write-Output "The user $User has been granted full control and ownership of the following folder(s)/file(s) $Path"
            add-content $LogFile "The user $User has been granted full control and ownership of the following folder(s)/file(s) $Path"
            }
        else{
        
            Write-Output "Warning! The Path $Path is not a valid direcoty or file"  
            Add-Content $LogFile "Warning! The Path $Path is not a valid direcoty or file"
            
            }
        
        }
        
}
catch {Write-Output $_.exception.message}