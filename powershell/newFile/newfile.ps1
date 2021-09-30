$count = 1
while ($count -lt 1001)
{
new-item -Path C:\Users\Administrator\Documents\Crypt\Vault4  -ItemType file -Name CryptFileVault4-$count.txt -value (Get-Content -Path C:\Users\Administrator\Documents\Strings\Vault4.txt -Raw)
$count++
}



