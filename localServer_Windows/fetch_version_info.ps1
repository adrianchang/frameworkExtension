Get-Date > .\last_update.txt 

Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Export-CSV -NoTypeInformation -Encoding UTF8 .\data\version1.csv 
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Export-CSV -NoTypeInformation -Encoding UTF8 .\data\version2.csv 


