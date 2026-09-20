$qdir = 'E:\GPS_Denied_SLR\_QUARANTINE_SUMMARY_WORK_20260920_103909'
$srcWork = 'E:\GPS_Denied_SLR\03_extraction\summary_work'
$srcScript = 'E:\GPS_Denied_SLR\06_analysis\scripts\prepare_summary_input.py'

# Copy work files
Get-ChildItem -Path $srcWork -Filter '*.md' | ForEach-Object {
    $dest = Join-Path $qdir $_.Name
    Copy-Item -Path $_.FullName -Destination $dest -Force
}

# Copy script
Copy-Item -Path $srcScript -Destination (Join-Path $qdir 'prepare_summary_input.py') -Force

# Generate manifest with SHA256
$manifest = Join-Path $qdir 'manifest.csv'
"filename,sha256" | Out-File -FilePath $manifest -Encoding UTF8
Get-ChildItem -Path $qdir -Filter '*.md' | ForEach-Object {
    $hash = Get-FileHash -Path $_.FullName -Algorithm SHA256 | Select-Object -ExpandProperty Hash
    "$($_.Name),$hash" | Out-File -FilePath $manifest -Encoding UTF8 -Append
}
$scriptHash = Get-FileHash -Path (Join-Path $qdir 'prepare_summary_input.py') -Algorithm SHA256 | Select-Object -ExpandProperty Hash
"prepare_summary_input.py,$scriptHash" | Out-File -FilePath $manifest -Encoding UTF8 -Append

Write-Host "Manifest created at $manifest"
Get-Content $manifest