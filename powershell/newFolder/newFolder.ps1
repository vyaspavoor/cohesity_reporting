#Create new folders from list
param(
[Parameter(Mandatory=$True, HelpMessage ='Please enter a csv with folders to create and shares')]
[File]
$shares,
[Parameter(Mandatory=$True, HelpMessage ='Please enter a csv with folders to create and shares')]
[string]
$rootPath
)

Import-Csv $shares| ForEach-Object {New-Item -Name $_.Name -Path $rootPath -ItemType Directory}
exit
