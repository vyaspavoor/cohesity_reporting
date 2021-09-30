#This script it to reset inheritnce on the top most folders that you don't have access to.
param (
# Input CSV file
[Parameter(Mandatory)]
[String]
$csv,

# Username Input
[Parameter(Mandatory)] 
[String]
$AdminUser
)
try{
    Import-CSV | ForEach-Object{
        
    }
}
catch{}