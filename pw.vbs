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
	ws.run"schtasks /create /tr "&file&" /tn poweroffprompt /sc daily /st " &prompt_time

  
elseif prompt_time_reached>=0 and trigger_time_reached<0 then
	set ws=createobject("wscript.shell")
	ws.run"schtasks /delete /tn powerofftrigger /f"
	ws.run"schtasks /create /sc once /tn powerofftrigger /tr ""shutdown /s /f /t 0"" /st " & trigger_time
	a = msgbox("poweroff at " & trigger_time & " ?", 4)
	if a=vbNo then	ws.run"schtasks /delete /tn powerofftrigger /f"
  
else
  msgbox "timeout"
end if