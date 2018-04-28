# cidrsmash

This will take a list of IPs from a file or stdin and condense them
into networks in CIDR notation.

## Examples
From stdin:
```
~/cidrsmash % nmap -n -sL 10.10.0.0/22 |grep "Nmap scan report for" |awk {'print $5'} |./cidrsmash.py -m 24
10.10.1.0/24
10.10.3.0/24
10.10.0.0/24
10.10.2.0/24
```

From a file:
```
~/cidrsmash % cat ips
10.0.0.1
10.0.0.2
10.0.0.3
10.0.0.4
10.1.0.1
~/cidrsmash % ./cidrsmash.py ips -m 16
10.0.0.0/16
10.1.0.0/16
```
