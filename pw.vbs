dim fso, file
dim prompt_time
dim trigger_time
dim current_time
dim prompt_time_reached
dim trigger_time_reached

set fso = CreateObject("Scripting.FileSystemObject")
set file = fso.GetFile(WScript.ScriptFullName)
prompt_time="16:59" rem 提示时间
trigger_time="17:00" rem 触发时间
current_time = FormatDateTime(Now, 3)
prompt_time_reached=datediff("n",CDate(prompt_time),current_time)
trigger_time_reached=datediff("n",CDate(trigger_time),current_time)

if prompt_time_reached<0 then
	set ws=createobject("wscript.shell")
	set objShell = createobject("Shell.Application")
	ws.run"schtasks /create /f /tn poweroffprompt /tr "&file&" /sc daily /st " &prompt_time,0
	objShell.ShellExecute "cmd.exe", "/c schtasks /create /f /tn powerofftrigger /tr ""shutdown /s /f /t 0"" /sc daily /st "&trigger_time&" /ru administrator /rp 123", "", "runas", 0
	
elseif prompt_time_reached>=0 and trigger_time_reached<0 then
	set ws=createobject("wscript.shell")
	set objShell = createobject("Shell.Application")
	rem ws.run"schtasks /create /sc once /tn powerofftrigger /tr ""shutdown /s /f /t 0"" /st " & trigger_time,0
	objShell.ShellExecute "cmd.exe", "/c schtasks /create /f /tn powerofftrigger /tr ""shutdown /s /f /t 0"" /sc daily /st "&trigger_time&" /ru administrator /rp 123", "", "runas", 0
	a = msgbox("poweroff at " & trigger_time & " ?", 32+4)
	if a=vbNo then	objShell.ShellExecute "cmd.exe", "/c schtasks /delete /f /tn powerofftrigger", "", "runas", 0
  
else
	msgbox "timeout"
end if