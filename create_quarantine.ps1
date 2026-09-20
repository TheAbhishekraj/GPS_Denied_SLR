$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$qdir = 'E:\GPS_Denied_SLR\_QUARANTINE_SUMMARY_WORK_' + $ts
New-Item -ItemType Directory -Path $qdir -Force | Out-Null
Write-Host $qdir