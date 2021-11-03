# Compare File Usage
---
This script is provided on a best effort basis.  It is expected that you have a working knowledge of PowerShell in order to run the script.  You may have to change  your execution policy in order to run this script.

# Download Files

```powershell
#Download Files
$scriptName = 'comparefolders'
$repoURL = 'https://raw.githubusercontent.com/greysave/cohesity/main/powershell'
(Invoke-WebRequest -Uri "$repo/$scriptName/$scriptName.ps1").content | Out-File "$scriptName.ps1"
```