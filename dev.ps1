function LodEnvVars {
    param (
        [Parameter(Position = 0)]
        [string]$envFile
    )
    if (Test-Path $envFile) {
        get-content $envFile | ForEach-Object {
            $name, $value = $_.split('=')
            set-content env:\$name $value
        }
    }
}

LodEnvVars "$PSScriptRoot\.env"

$env:PATH="$env:PATH;$env:POSTGRES_BIN"
uv run main.py $args