# Compare File Read Me
---
This script is provided on a best effort basis.  It is expected that you have a working knowledge of PowerShell in order to run the script.  You may have to change  your execution policy in order to run this script.

This script looks for missing files between a soure and target.  If a file is missing at the target then the file will be flagged.If used after a migration it also checks the MD5 has for corruption between the source and target.  If the file has corrupted during a move/copy at the target then that file will be flagged.

## Download Files

```powershell
#Download Files
$scriptName = 'compareFolders'
$repoURL = 'https://raw.githubusercontent.com/greysave/cohesity/main/powershell'
(Invoke-WebRequest -Uri "$repo/$scriptName/$scriptName.ps1").content | Out-File "$scriptName.ps1"
```

## Script Pre-requisites
You need to mount the source and target volumes in powershell using the following command.
Note that if you don't' want the mapping to persist after reboots you should remove the persist.  Please see the following micrsoft page for more information on mounting drives in powershell.  [New-PSDrive](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-psdrive?view=powershell-7.1 'New-PSDrive')

# Map Network Drive Commands
```PowerShell
#Source
New-PSDrive –Name “S” –PSProvider FileSystem –Root “\\SMB-Server\share” –Persist

#Target
New-PSDrive –Name “T” –PSProvider FileSystem –Root “\\SMB-Server\share” –Persist
```  

