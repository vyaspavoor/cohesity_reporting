$count = 1
while ($count -lt 1001)
{
new-item -Path C:\Users\Administrator\Documents\Crypt\Vault2  -ItemType file -Name MurphWin2CryptFileVault2-$count.txt -value (Get-Content -Path C:\Users\Administrator\Documents\Strings\Vault2.txt -Raw)
$count++
}

