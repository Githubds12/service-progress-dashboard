$TaskName = "StartAutoServersAdmin"
$TaskPath = "C:\HTB-Notes-Portal\StartAutoServers.bat"
$TaskDescription = "Runs the HTB-Notes-Portal Auto Servers with Highest Privileges on Logon."

# Define the action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$TaskPath`"" -WorkingDirectory "C:\HTB-Notes-Portal"

# Define the trigger (On Logon)
$Trigger = New-ScheduledTaskTrigger -AtLogon

# Define the principal (Run as Admin)
$Principal = New-ScheduledTaskPrincipal -UserId "Gorri" -LogonType Interactive -RunLevel Highest

# Define settings (Allow start on demand, don't stop if running, etc.)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task (overwrite if exists)
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description $TaskDescription

Write-Host "Successfully created Scheduled Task: $TaskName"
