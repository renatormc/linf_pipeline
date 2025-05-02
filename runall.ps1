if (Test-Path .\.local\results.json) {
    Remove-Item -Path .\.local\results.json
}

foreach ($i in 1..6) {
    Write-Host "Running simulation for scene $i"
    uv run .\main.py simulate $i --restore
}
