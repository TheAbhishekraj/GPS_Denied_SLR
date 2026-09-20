# Delete original files
Remove-Item -Path 'E:\GPS_Denied_SLR\03_extraction\summary_work' -Recurse -Force
Remove-Item -Path 'E:\GPS_Denied_SLR\06_analysis\scripts\prepare_summary_input.py' -Force

# Verify
Write-Host "summary_work exists: $(Test-Path 'E:\GPS_Denied_SLR\03_extraction\summary_work')"
Write-Host "prepare_summary_input.py exists: $(Test-Path 'E:\GPS_Denied_SLR\06_analysis\scripts\prepare_summary_input.py')"
Write-Host "per_paper files:"
Get-ChildItem -Path 'E:\GPS_Denied_SLR\03_extraction\per_paper' -Filter '*.md' | Select-Object Name
Write-Host "MASTER_EVIDENCE.csv rows:"
$csv = Import-Csv 'E:\GPS_Denied_SLR\02_data_processed\MASTER_EVIDENCE.csv'
Write-Host $csv.Count