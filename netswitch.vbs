Sub Wlanon()
	objShell.ShellExecute "cmd.exe", "/c netsh interface set interface ""wlan"" enabled & netsh interface set interface ""eth0"" disabled", "", "runas", 0
	WshShell.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyEnable", 0, "REG_DWORD"
End Sub

Sub Wlanoff()
	objShell.ShellExecute "cmd.exe", "/c netsh interface set interface ""wlan"" disabled & netsh interface set interface ""eth0"" enabled", "", "runas", 0
	ProxyServer = "192.168.0.24:6888"
	WshShell.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyServer", ProxyServer, "REG_SZ"
	WshShell.RegWrite "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyEnable", 1, "REG_DWORD"
End Sub

Set WshShell = WScript.CreateObject("WScript.Shell")
Set objshell=createobject("Shell.Application")
Set objWMIService = GetObject("winmgmts:\\.\root\CIMV2")
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_NetworkAdapter WHERE NetConnectionStatus = 2")
Dim ethstate
ethstate=0
For Each objItem In colItems
    if objItem.Name="Realtek PCIe GbE Family Controller" then
    ethstate=1
    end if
Next

if ethstate=0 then
	Wlanoff
elseif ethstate=1 then
	Wlanon
end if