foreach ($i in 1..6) {
    Write-Host "Running simulation for scene $i"
    uv run .\main.py simulate $i --restore
}
