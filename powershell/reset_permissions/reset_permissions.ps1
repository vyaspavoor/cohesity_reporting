param (
# CSV Input
[Parameter(Mandatory)]
[String]
$csv,

# Username Input
[Parameter(Mandatory)] 
[String]
$AdminUser,

# Hostname
[Parameter(Mandatory)]
[String]
$HostName,

# Share hame
[Parameter(Mandatory)]
[String]
$Share
)
$ErrorActionPreference = "Continue";
try {
    $FileName = (Get-Date).tostring("dd-MM-yyyy-hh-mm-ss")
    $LogFile = New-Item -itemType File -Name ("PermissionChangeLog_" + $FileName + ".log")
    Import-Csv $csv | ForEach-Object{
        #Ownership and Permission Change
        if ($_.'Error Message'.contains('[kPermissionDenied]')){
            $OriginalPath = $_.'File Path'
            $NewPath = $OriginalPath -replace '/', '\'
            $Path = "\\" + $HostName + '\' + $Share + $NewPath
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
}
catch {Write-Output $_.exception.message}