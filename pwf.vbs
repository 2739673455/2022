Dim fso, file
Dim username, password
Dim prompttime, triggertime
username="system"
password="123"
prompttime="16:59:00" rem 提示时间
triggertime="17:00:00" rem 触发时间

Set args = WScript.Arguments
Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.GetFile(WScript.ScriptFullName)

Sub CreateScheduledTask3()
	Dim service
	Set service = CreateObject("Schedule.Service")
	call service.Connect()
	
	Dim rootFolder
	Set rootFolder = service.GetFolder("\")

	Dim taskDefinition
	Set taskDefinition = service.NewTask(0) 

	Dim regInfo
	Set regInfo = taskDefinition.RegistrationInfo

	Dim settings
	Set settings = taskDefinition.Settings
	settings.Enabled = True
	settings.StartWhenAvailable = True
	settings.WakeToRun = True

	Dim trigger
	Set trigger = taskDefinition.Triggers.Create(2)

	Dim startTime
	startTime = "2023-01-01T"&triggertime
	trigger.StartBoundary = startTime

	Dim Action
	Set Action = taskDefinition.Actions.Create(0)
	Action.Path = "shutdown"
	Action.Arguments = "/s /f /t 0"

	call rootFolder.RegisterTaskDefinition("pwftrigger",taskDefinition,6,username,,1)
End Sub

if args.Count=0 then
	Set ws=createobject("wscript.shell")
	set objShell = createobject("Shell.Application")
	objShell.ShellExecute "cmd.exe", "/c schtasks /create /tn pwflogon /tr """&file&" 0"" /sc onlogon /f", "", "runas", 0
	ws.run"schtasks /create /tn pwfprompt /tr """&file&" 1"" /sc daily /st "&prompttime&" /f", 0
	objShell.ShellExecute "cmd.exe", "/c """&file&" 2""", "", "runas", 0
elseif args(0)=0 then
	set objShell = createobject("Shell.Application")
	objShell.ShellExecute "cmd.exe", "/c """&file&" 2""", "", "runas", 0
elseif args(0)=1 then
	set objShell = createobject("Shell.Application")
	resp = msgbox("Poweroff At " & triggertime & " ?", 4096+32+4)
	if resp=vbNo then objShell.ShellExecute "cmd.exe", "/c schtasks /delete /tn pwftrigger /f", "", "runas", 0
elseif args(0)=2 then
	CreateScheduledTask3
end if