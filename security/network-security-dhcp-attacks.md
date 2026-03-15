# DHCP Attacks & Mitigation Guide

> **Disclaimer:** This document is provided for educational and informational purposes only. The authors and contributors shall not be held liable for any damages, losses, or claims arising from the use or misuse of the information contained herein. Readers assume full responsibility for their actions. Apply these concepts only in environments where you have explicit authorization.

---

## Table of Contents

1. [The DHCP Protocol](#1-the-dhcp-protocol)
2. [DHCP Starvation Attack](#2-dhcp-starvation-attack)
3. [DHCP Rogue Server Attack](#3-dhcp-rogue-server-attack)
4. [Mitigation: DHCP Snooping](#4-mitigation-dhcp-snooping)
5. [Mitigation: IP Source Guard](#5-mitigation-ip-source-guard)
6. [Quick Reference](#6-quick-reference)

---

## 1. The DHCP Protocol

The **Dynamic Host Configuration Protocol (DHCP)** enables devices to automatically obtain IP addresses and network configuration parameters from a DHCP server, eliminating the need for manual configuration on each host.

### DORA Sequence

A typical IP address acquisition follows a four-step process known as **DORA** (Discover, Offer, Request, Acknowledge):

```
DHCP Client                         DHCP Server
    |                                     |
    | -------- DHCP Discover (broadcast) -------> |
    |                                     |
    | <------- DHCP Offer (unicast/broadcast) --- |
    |                                     |
    | -------- DHCP Request (broadcast) --------> |
    |                                     |
    | <------- DHCP Ack (unicast) --------------- |
    |                                     |
    | -------- DHCP Release (unicast) ----------> |
    |                                     |
```

### DHCP Message Types

| Message | Direction | Description |
|---------|-----------|-------------|
| **DHCP Discover** | Client → Server (broadcast) | Sent to locate available DHCP servers on the network. |
| **DHCP Offer** | Server → Client | The server responds to a Discover with a proposed IP configuration. This frame may be sent as **unicast** or **broadcast**, depending on the broadcast flag set by the client in the Discover message. Contains the offered IP address, subnet mask, default gateway, DNS servers, and lease duration. |
| **DHCP Request** | Client → Server (broadcast) | The client broadcasts its acceptance of one server's offer. Broadcasting (rather than unicasting) ensures that **all** DHCP servers are informed of the decision, allowing unselected servers to reclaim their offered addresses. |
| **DHCP Ack** | Server → Client (unicast) | The selected server confirms the IP assignment and delivers the final configuration parameters. |
| **DHCP Nack** | Server → Client | The server rejects the client's request — typically because the requested IP is no longer available or the client has moved to a different subnet. |
| **DHCP Decline** | Client → Server | The client rejects the offered IP address, usually because it has detected an IP conflict via ARP. |
| **DHCP Release** | Client → Server (unicast) | The client voluntarily returns its IP address before the lease expires. |
| **DHCP Inform** | Client → Server (unicast) | The client already has an IP address but requests additional configuration parameters (e.g., DNS, NTP servers). |

> **Note:** The DHCP Offer frame carries more than just an IP address — it includes the subnet mask, default gateway, DNS server addresses, domain name, and lease time. These parameters are what make DHCP a powerful (and potentially dangerous) configuration vector.

For deeper protocol details, refer to [RFC 2131](https://datatracker.ietf.org/doc/html/rfc2131) or the [Wikipedia article on DHCP](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol).

---

## 2. DHCP Starvation Attack

### Concept

A DHCP starvation attack aims to exhaust a DHCP server's available IP address pool by flooding it with requests, each spoofing a different MAC address. Once the pool is depleted, legitimate clients attempting to join the network are denied an IP address.

### Attack Flow

```
Attacker                      DHCP Server
    |                              |
    |-- Discover (MAC: AA:BB:..) ->|  Allocates 192.168.1.101
    |-- Discover (MAC: CC:DD:..) ->|  Allocates 192.168.1.102
    |-- Discover (MAC: EE:FF:..) ->|  Allocates 192.168.1.103
    |         ...                  |       ...
    |-- Discover (MAC: XX:YY:..) ->|  Pool exhausted — NO IP AVAILABLE
    |                              |
 Legitimate Client                 |
    |-- Discover ----------------->|  NO RESPONSE (pool empty)
    |                              |
```

Once the legitimate server is starved, the attacker can introduce a **rogue DHCP server** (see below) to serve new clients with malicious configuration — positioning themselves as the default gateway to enable Man-in-the-Middle (MITM) attacks. Since DHCP leases include the default gateway and DNS server addresses, a rogue server can redirect all victim traffic through the attacker's machine.

### Tool: Yersinia

[Yersinia](https://github.com/tomac/yersinia) is a Layer 2 attack framework that supports multiple protocols, including DHCP, STP, CDP, and more.

**Launch a DHCP starvation attack:**

```bash
# -attack 1 = DoS via DHCP Discover flooding
yersinia dhcp -attack 1 -interface eth0
```

| Flag | Description |
|------|-------------|
| `dhcp` | Specifies the DHCP protocol module. |
| `-attack 1` | DoS attack — floods the network with DHCP Discover packets using spoofed MAC addresses. |
| `-interface eth0` | Specifies the network interface to use for sending the attack traffic. |

**Stop the attack:**

```bash
killall yersinia
```

---

## 3. DHCP Rogue Server Attack

### Concept

A rogue DHCP server is an unauthorized server introduced into the network to respond to client DHCP requests with malicious configuration. The attacker's goal is to **respond faster** than the legitimate DHCP server, causing clients to accept the rogue server's lease.

### How to Win the Race

The attacker must be faster **twice**:

1. **Reply to the DHCP Discover** — be the first to send a DHCP Offer.
2. **Send the DHCP Ack** — be the first to confirm the lease after the client's Request.

Several strategies improve the odds:

| Strategy | Explanation |
|----------|-------------|
| **DoS the legitimate server** | A DHCP starvation attack (see above) burdens the real server, increasing its response time and giving the rogue server an edge. |
| **Lightweight DHCP implementation** | A minimal, purpose-built DHCP server running on the attacker's machine can respond faster than a full-featured server (which also handles DNS, gateway functions, lease database lookups, etc.). By hard-coding the response and skipping cache validation, the rogue server achieves minimal latency. |
| **Network placement** | Positioning the rogue server closer to clients (fewer hops) reduces propagation delay. |

### Tool: Yersinia

**Launch a rogue DHCP server attack:**

```bash
# -attack 2 = Non-DoS rogue DHCP server
yersinia dhcp -attack 2 -interface eth0
```

| Flag | Description |
|------|-------------|
| `-attack 2` | Creates a rogue DHCP server that responds to client Discover requests without requiring a prior DoS attack. Its streamlined implementation is typically faster than standard DHCP servers found on home/office routers. |

> **Note:** In practice, combining both attacks (starvation + rogue server) is the most effective approach — the starvation attack suppresses the legitimate server while the rogue server handles all new requests.

---

## 4. Mitigation: DHCP Snooping

DHCP Snooping is a Layer 2 security feature available on Cisco switches (and other vendors) that filters untrusted DHCP messages and maintains a **DHCP Snooping Binding Table** — a database mapping MAC addresses, IP addresses, lease durations, VLAN IDs, and physical interfaces.

### How It Works

Switch ports are classified into two categories:

| Port Type | Behavior |
|-----------|----------|
| **Trusted** | Permits DHCP Offer, Ack, Nack, and all other DHCP messages. Used on ports connected to known DHCP servers or uplink ports toward the server. |
| **Untrusted** | Only permits DHCP Discover and DHCP Request messages inbound. Drops DHCP Offer, Ack, Nack, and Release packets. Used on all client-facing access ports. |

When a client receives a valid IP from a DHCP server (via a trusted port), the switch records the binding in the snooping table. Any DHCP Offer or Ack arriving on an **untrusted** port is dropped — preventing rogue servers from operating.

### The Binding Table

The DHCP Snooping Binding Table is stored in **DRAM** (volatile memory) by default. This means:

- The table is **lost on reboot**, requiring clients to re-obtain leases.
- On large networks, the table can consume significant memory and generate notable CPU load during updates.
- For persistence and scalability, the table should be offloaded to an external database agent.

**Configure remote database storage:**

```
Cisco(config)# ip dhcp snooping database ftp://192.168.42.69/binding-table.dhcp
Cisco(config)# ip dhcp snooping database write-delay 300
```

| Command | Description |
|---------|-------------|
| `ip dhcp snooping database <url>` | Specifies the remote URL where the binding table will be stored. Supports FTP, HTTP, RCP, and TFTP. |
| `write-delay 300` | Sets a **300-second delay** before writing changes to the remote database. This batches updates to avoid excessive I/O operations when the table changes frequently. |

### Full Configuration Example

```
! Step 1: Enable DHCP Snooping globally
Cisco(config)# ip dhcp snooping

! Step 2: Enable DHCP Snooping on specific VLANs
Cisco(config)# ip dhcp snooping vlan 10,20,30

! Step 3: Configure the trusted port (connected to the legitimate DHCP server)
Cisco(config)# interface GigabitEthernet1/0/1
Cisco(config-if)# ip dhcp snooping trust

! Step 4: (Optional) Set rate limiting on untrusted ports to prevent flooding
Cisco(config)# interface GigabitEthernet1/0/2
Cisco(config-if)# ip dhcp snooping limit rate 15

! Step 5: (Optional) Configure remote database storage
Cisco(config)# ip dhcp snooping database tftp://192.168.42.69/binding-table.dhcp
Cisco(config)# ip dhcp snooping database write-delay 300
```

> **Best Practice:** Apply rate limiting (`limit rate`) on untrusted access ports. This prevents a starvation attack from generating excessive DHCP traffic, even if the attacker bypasses other controls. A typical value is 15 packets per second for access ports.

---

## 5. Mitigation: IP Source Guard

IP Source Guard builds on DHCP Snooping to prevent **IP spoofing** — an attack where a malicious host changes its IP and/or MAC address to impersonate another device, bypass ACLs, or gain unauthorized access.

### How It Works

IP Source Guard uses the DHCP Snooping Binding Table to enforce that traffic originating from a switch port matches the expected IP and MAC address pair.

1. **Before DHCP assignment:** All non-DHCP traffic on the port is dropped. Only DHCP packets are permitted, allowing the client to obtain a legitimate lease.
2. **After DHCP assignment:** Once the snooping table records the binding, a **Port ACL (PACL)** is dynamically installed on the port. Only traffic matching the source IP (and optionally MAC) from the binding table is permitted.
3. **Spoofing attempt:** Any traffic with a different source IP or MAC is immediately dropped at the port level.

### Configuration

```
Cisco(config)# interface FastEthernet1/0/3
Cisco(config-if)# ip verify source port-security
```

| Command | Description |
|---------|-------------|
| `ip verify source` | Enables IP Source Guard — filters traffic based on source IP address matching the DHCP snooping binding table. |
| `port-security` | Adds MAC address filtering in addition to IP filtering. When combined with port security, both source IP **and** source MAC must match the binding table entry. |

> **Prerequisite:** DHCP Snooping **must** be enabled and functioning before IP Source Guard will work. IP Source Guard is dependent on the binding table populated by DHCP Snooping. If the table is empty, all non-DHCP traffic will be dropped.

---

## 6. Quick Reference

### Attack Summary

| Attack | Tool | Command | Impact |
|--------|------|---------|--------|
| DHCP Starvation | Yersinia | `yersinia dhcp -attack 1 -interface eth0` | Exhausts IP pool; denies service to new clients |
| Rogue DHCP Server | Yersinia | `yersinia dhcp -attack 2 -interface eth0` | Distributes malicious config; enables MITM |

### Mitigation Summary

| Feature | Protects Against | Key Command | Depends On |
|---------|-----------------|-------------|------------|
| DHCP Snooping | Rogue DHCP servers, starvation flooding | `ip dhcp snooping` + `ip dhcp snooping vlan <id>` + `ip dhcp snooping trust` | None |
| IP Source Guard | IP spoofing, MAC spoofing | `ip verify source port-security` | DHCP Snooping (binding table) |
| Rate Limiting | DHCP flood attacks | `ip dhcp snooping limit rate <pps>` | DHCP Snooping |

---
