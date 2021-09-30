$vault = "c:\Users\Administrator\Documents\Crypt\Vault1*"
$key= (get-content -path "c:\Users\Administrator\Documents\Keys\cryptkey1.txt" -Raw)

get-childitem -path $vault -recurse | % { Protect-File -KeyAsPlainText $key $_ }
