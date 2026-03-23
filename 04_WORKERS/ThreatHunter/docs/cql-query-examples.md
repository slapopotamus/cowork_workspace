# CrowdStrike CQL — Real-World Query Examples
### ThreatHunter Knowledge Base | docs/cql-query-examples.md

> **Sources:** ByteRay-Labs/Query-Hub (github.com/ByteRay-Labs/Query-Hub); LogScale Documentation v1.229.0–1.232.0
> **Last updated:** 2026-03-23
> **See also:** [cql-syntax.md](cql-syntax.md) for language reference

These are production-grade CQL queries illustrating advanced techniques: multi-event joins, rate calculations, XML parsing, geo-enrichment, recursive base64 decoding, and time-bucketed clustering. Each entry includes MITRE ATT&CK context where applicable.

---

## Table of Contents

1. [Credential Dumping Detection](#1-credential-dumping-detection)
2. [Failed Logon Thresholding (Brute Force)](#2-failed-logon-thresholding-brute-force)
3. [Detect and Decode Base64-Encoded PowerShell](#3-detect-and-decode-base64-encoded-powershell)
4. [LOLBin: Certutil Download Detection](#4-lolbin-certutil-download-detection)
5. [Lateral Movement via Network Ports](#5-lateral-movement-via-network-ports)
6. [Connections to Tor Exit Nodes](#6-connections-to-tor-exit-nodes)
7. [Frequency Analysis — Recon Tool Clustering](#7-frequency-analysis--recon-tool-clustering)
8. [DNS Staging Detection (ClickFix-Inspired)](#8-dns-staging-detection-clickfix-inspired)
9. [Hidden Scheduled Tasks](#9-hidden-scheduled-tasks)
10. [File Write Events with Human-Readable Sizes](#10-file-write-events-with-human-readable-sizes)
11. [Impossible Travel Time (Azure SSO)](#11-impossible-travel-time-azure-sso)

---

## 1. Credential Dumping Detection

**MITRE:** T1003.001 (LSASS Memory), T1003.002 (SAM), T1558.003 (Kerberoasting)

Detects execution of known credential dumping tools by command line content or image filename. Enriches with user identity and parent process hash via dual joins.

**Key techniques used:** Multi-join enrichment using `UserIdentity` and `SyntheticProcessRollup2`; `join(..., suffix=)` to avoid field collision on parent process data.

```logscale
#event_simpleName=ProcessRollup2
| (CommandLine=/mimikatz|procdump|lsass|sekurlsa/i OR ImageFileName=/\\(mimikatz|procdump|pwdump)\.exe$/i)
| ParentImageFileName!=/\\(powershell|cmd)\.exe$/i
| join({#event_simpleName=UserIdentity}, field=AuthenticationID, include=[UserName])
| join({#event_simpleName=SyntheticProcessRollup2}, field=[aid, RawProcessId], include=[SHA256HashData], suffix="Parent")
| table([aid, UserName, ImageFileName, CommandLine, ParentImageFileName, SHA256HashData])
```

**Notes:**
- `UserIdentity` is an enrichment event type — joinable on `AuthenticationID`
- `suffix="Parent"` prevents field name collision when joining parent process data
- Adjust `ParentImageFileName` exclusion filter to match your environment's baseline

---

## 2. Failed Logon Thresholding (Brute Force)

**MITRE:** T1110 (Brute Force)

Identifies accounts with more than 5 failed logon attempts, calculates the failure rate per hour, and converts sub-status codes to readable hex. Useful for detecting both targeted brute force and password spray patterns.

**Key techniques used:** Hex format conversion with `format()` + `upper()`; delta time calculation with arithmetic on epoch timestamps; `$falcon/helper:enrich()` for sub-status/logon type enrichment.

```logscale
// Get Windows UserLogonFailed events
event_platform=Win #event_simpleName=UserLogonFailed2

// Convert SubStatus to readable hex
| SubStatus_hex := format(field=SubStatus, "%x")
| SubStatus_hex := upper(SubStatus_hex)
| SubStatus_hex := format(format="0x%s", field=[SubStatus_hex])

// Aggregate: count failures, capture time range, collect IPs
| groupBy([aid, ComputerName, UserName, LogonType, SubStatus_hex, SubStatus],
    function=([count(aid, as=FailCount),
               min(ContextTimeStamp, as=FirstLogonAttempt),
               max(ContextTimeStamp, as=LastLogonAttempt),
               collect([LocalAddressIP4, aip])]))

// Rate calculation
| firstLastDeltaHours := ((LastLogonAttempt - FirstLogonAttempt) / 60 / 60)
| round("firstLastDeltaHours")
| logonAttemptsPerHour := (FailCount / firstLastDeltaHours)
| round("logonAttemptsPerHour")

// Convert epoch timestamps to human-readable
| FirstLogonAttempt := formatTime(format="%F %T.%L", field="FirstLogonAttempt")
| LastLogonAttempt  := formatTime(format="%F %T.%L", field="LastLogonAttempt")

// Apply threshold and sort
| FailCount > 5
| sort(FailCount, order=desc, limit=2000)
| $falcon/helper:enrich(field=LogonType)
| $falcon/helper:enrich(field=SubStatus)
```

**Notes:**
- `ContextTimeStamp` is epoch seconds — arithmetic produces seconds; divide by `60/60` for hours
- `$falcon/helper:enrich()` is a Falcon-provided saved search for enriching Logon Type and NTSTATUS codes
- Tune the `FailCount > 5` threshold based on your environment's expected authentication patterns
- For password spray detection, modify to group by `SubStatus` and look for broad username spread with low per-account count

---

## 3. Detect and Decode Base64-Encoded PowerShell

**MITRE:** T1059.001 (PowerShell), T1027 (Obfuscated Files or Information)

Detects encoded PowerShell, counts unique execution instances, decodes the base64 payload, and handles nested double-encoding using a `case` statement.

**Key techniques used:** `base64Decode()` with `charset="UTF-16LE"` for Windows PowerShell encoding; `splitString()` to isolate the encoded argument; nested `case` for double-encoded payloads.

```logscale
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/.*\\powershell\.exe/
| CommandLine=/\s+\-(e|encoded|encodedcommand|enc)\s+/i

// Extract the flag variant used
| CommandLine=/\-((?<psEncFlag>(e|encoded|encodedcommand|enc)))\s+/i
| length("CommandLine", as="cmdLength")

// Aggregate — count unique endpoints and total executions
| groupBy([psEncFlag, cmdLength, CommandLine],
    function=stats([count(aid, distinct=true, as="uniqueEndpointCount"),
                    count(aid, as="executionCount")]), limit=max)

// Decode first layer
| EncodedString  := splitString(field=CommandLine, by="-e* ", index=1)
| DecodedString  := base64Decode(EncodedString, charset="UTF-16LE")

// Handle nested double-encoding
| case {
    DecodedString = /encoded/i
    | SubEncodedString := splitString(field=DecodedString, by="-EncodedCommand ", index=1)
    | SubDecodedString := base64Decode(SubEncodedString, charset="UTF-16LE");
    *
}

| table([executionCount, uniqueEndpointCount, cmdLength, DecodedString, CommandLine])
| sort(executionCount, order=desc)
```

**Notes:**
- `charset="UTF-16LE"` is required — PowerShell encodes commands in UTF-16 Little Endian, not UTF-8
- The catch-all `*` in the `case` block ensures events without nested encoding pass through without being dropped
- High `uniqueEndpointCount` on a single encoded command is a strong lateral movement or ransomware distribution indicator

---

## 4. LOLBin: Certutil Download Detection

**MITRE:** T1105 (Ingress Tool Transfer), T1564.004 (NTFS File Attributes), T1027.013 (Encrypted/Encoded File), T1140 (Deobfuscate/Decode)

Detects `certutil.exe` used to download content from HTTP/HTTPS URLs — a classic LOLBin abuse pattern.

```logscale
in(#event_simpleName, values=["ProcessRollup2", "ProcessBlocked"])
| event_platform=Win
| ImageFileName=/certutil.exe/i
| CommandLine=/(https?:)/i
```

**Notes:**
- Including `ProcessBlocked` catches cases where policy prevented execution but the attempt is still logged
- For broader LOLBin coverage, extend the `ImageFileName` filter to other known downloaders: `bitsadmin.exe`, `mshta.exe`, `regsvr32.exe`, `wscript.exe`

---

## 5. Lateral Movement via Network Ports

**MITRE:** T1021.001 (RDP), T1021.002 (SMB/Windows Admin Shares), T1135 (Network Share Discovery)

Detects outbound connections to lateral movement ports (RDP, SMB, WinRM) from non-RFC1918 space, enriched with the process and user identity responsible.

**Key techniques used:** `!cidr()` negation for RFC1918 exclusion; multi-join to correlate network events with process and user identity.

```logscale
#event_simpleName=NetworkConnect
| (RemotePort=445 OR RemotePort=3389 OR RemotePort=5985)
| !cidr(RemoteAddressIP4, subnet=["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"])
| join({#event_simpleName=ProcessRollup2}, field=[aid, RawProcessId], include=[ImageFileName, CommandLine])
| join({#event_simpleName=UserIdentity}, field=AuthenticationID, include=[UserName])
| table([aid, UserName, ImageFileName, RemoteAddressIP4, RemotePort, CommandLine])
```

**Notes:**
- Uses `NetworkConnect` (not `NetworkConnectIP4`) — verify which event type is available in your environment
- Add `LocalAddressIP4` to the output table to help identify the source machine within the network
- Port 5985 is WinRM HTTP; also consider adding 5986 (WinRM HTTPS) and 22 (SSH) for broader coverage

---

## 6. Connections to Tor Exit Nodes

**MITRE:** T1090.003 (Proxy — Multi-hop Proxy)

Correlates endpoint network connections against a Tor exit node lookup file to identify C2 or exfiltration over Tor.

**Key techniques used:** `match(file=...)` for lookup file enrichment; `collect()` with `min()`/`max()` for time-bounding per host.

```logscale
#event_simpleName=NetworkConnectIP4
| match(file="tor-exit-nodes.csv", field=RemoteAddressIP4, column=ip, strict=true)
| groupBy([aid, ComputerName],
    function=[count(aid, as=ConnectionCount),
              count(aid, distinct=true, as=UniqueIPs),
              collect([RemoteAddressIP4, RemotePort]),
              min(@timestamp, as=FirstSeen),
              max(@timestamp, as=LastSeen)])
| FirstSeen := formatTime(format="%Y-%m-%d %H:%M:%S", field=FirstSeen)
| LastSeen  := formatTime(format="%Y-%m-%d %H:%M:%S", field=LastSeen)
| sort(ConnectionCount, order=desc)
```

**Notes:**
- Requires a `tor-exit-nodes.csv` lookup file uploaded to the LogScale repository with an `ip` column
- `strict=true` drops events where the IP is not in the lookup — set to `strict=false` to keep all events and use the match as enrichment only
- Maintain the lookup file regularly; Tor exit nodes rotate frequently

---

## 7. Frequency Analysis — Recon Tool Clustering

**MITRE:** T1082 (System Information Discovery), T1083 (File and Directory Discovery), T1069 (Permission Groups Discovery), T1087 (Account Discovery)

Detects adversary discovery/enumeration activity by identifying time-clustered execution of 3+ distinct reconnaissance tools within a 10-minute window.

**Key techniques used:** `bucket()` for time-windowed aggregation; `count(FileName, distinct=true)` to count unique tool names; `test()` for threshold filtering on aggregated results.

```logscale
event_platform=Win #event_simpleName=ProcessRollup2
| FileName=/(whoami|arp|cmd|net|net1|ipconfig|route|netstat|nslookup|nltest|
              systeminfo|wmic|tasklist|tracert|ping|adfind|nbtstat|find|
              ldifde|netsh|wbadmin)\.exe/i

// Bucket by 10-minute windows, grouped by host and parent process
| bucket(span=10min, field=[cid, aid, ComputerName, ParentBaseFileName, ParentProcessId],
    function=[count(FileName, distinct=true, as=fNameCount),
              collect([FileName, CommandLine])], limit=500)

// Alert when 3+ distinct recon tools run in a single window
| test(fNameCount >= 3)
```

**Notes:**
- Grouping by `ParentBaseFileName` and `ParentProcessId` keeps clusters scoped to a single parent — reduces noise from administrators legitimately running multiple tools
- Tune the `fNameCount >= 3` threshold; 4+ may reduce false positives in environments with scripted baseline tooling
- The `limit=500` in `bucket()` caps collected command lines — increase if needed for high-volume environments

---

## 8. DNS Staging Detection (ClickFix-Inspired)

**MITRE:** T1071.004 (DNS Application Layer Protocol), T1059.001 (PowerShell), T1204.002 (Malicious File)

Detects `nslookup` used to query TXT records or specific DNS servers — a pattern observed in ClickFix-style social engineering attacks that stage payloads via DNS TXT records.

```logscale
#event_simpleName = ProcessRollup2
| ImageFileName = /\\nslookup\.exe$/i

// Non-default DNS server or TXT record queries
| CommandLine = /nslookup.*(-q|querytype)=(txt|all)/i
    or CommandLine = /nslookup.* \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/

// Exclude known-good parents
| ParentBaseFileName != /services\.exe|monitoring_agent\.exe/i

| groupBy([ComputerName, UserName, CommandLine], function=count())
| table([ComputerName, UserName, CommandLine, _count])
```

**Notes:**
- TXT record queries from endpoint processes are highly anomalous outside of specific IT/monitoring tooling
- The IP-as-argument pattern catches queries routed to attacker-controlled DNS resolvers
- Expand the `ParentBaseFileName` exclusion list to match your environment's legitimate DNS tooling

---

## 9. Hidden Scheduled Tasks

**MITRE:** T1053.005 (Scheduled Task/Job)

Detects scheduled tasks configured with `Hidden=true` in their XML definition — a persistence evasion technique that suppresses the task from the Task Scheduler UI.

**Key techniques used:** `parseXml()` to extract structured data from the `TaskXml` field; field rename from nested XML path.

```logscale
#event_simpleName=ScheduledTaskRegistered
| parseXml(TaskXml)
| Hidden := rename(Task.Settings.Hidden)
| Hidden = /true/i
| table([aid, Hidden, TaskXml], limit=1000)
```

**Notes:**
- `parseXml()` extracts the full task definition into queryable fields
- `Task.Settings.Hidden` is the XML path to the hidden flag — path varies by task XML schema version
- Consider extending to also flag tasks with `ExecutionTimeLimit=PT0S` (no time limit) or pointing to `%TEMP%`/user-writable paths

---

## 10. File Write Events with Human-Readable Sizes

**MITRE:** Context-dependent (data staging, exfiltration baselining)

Demonstrates `unit:convert()` and `case` branching for converting raw byte counts into human-readable file sizes. Useful for data staging and exfiltration volume analysis.

**Key techniques used:** `unit:convert()` for byte-to-unit conversion; `case` for tiered size labeling; `format()` for formatted number strings.

```logscale
#event_simpleName=/FileWritten$/
| case {
    Size>=1099511627776 | CommonSize := unit:convert(Size, to=T) | format("%,.2f TB", field=["CommonSize"], as="CommonSize");
    Size>=1073741824    | CommonSize := unit:convert(Size, to=G) | format("%,.2f GB", field=["CommonSize"], as="CommonSize");
    Size>=1048576       | CommonSize := unit:convert(Size, to=M) | format("%,.2f MB", field=["CommonSize"], as="CommonSize");
    Size>1024           | CommonSize := unit:convert(Size, to=k) | format("%,.3f KB", field=["CommonSize"], as="CommonSize");
    *                   | CommonSize := format("%,.0f Bytes", field=["Size"]);
}
| table([@timestamp, aid, ComputerName, FileName, Size, CommonSize])
```

**Notes:**
- Use `#event_simpleName=/FileWritten$/` (trailing `$` anchors to end of string) to avoid matching variants like `FileWrittenPending`
- The `*` catch-all ensures files under 1KB are captured; without it, unmatched events are dropped from `case`
- Extend with `groupBy([ComputerName, UserName])` and `sum(Size)` to aggregate total write volume per host for exfiltration baselining

---

## 11. Impossible Travel Time (Azure SSO)

**MITRE:** T1078.004 (Valid Accounts — Cloud Accounts)

Identifies logins from geographically impossible locations within a short time window by calculating travel speed between consecutive login geolocations. Flags logins requiring travel faster than 900 km/h across different countries.

**Key techniques used:** `neighbor()` to retrieve the previous event for each user; `ipLocation()` for geo-enrichment; `geography:distance()` for distance calculation; `crypto:md5()` for user hashing; `formatDuration()` for human-readable time deltas.

```logscale
in(field="#event_simpleName", values=[SsoApplicationAccess, SsoUserLogon])
| ClientUserAgentString != /ios /i and ClientUserAgentString != /Safari/i
| !cidr(SourceEndpointAddressIP4, subnet=["0.0.0.0/16"])

// Build consistent user identifier
| SourceIP   := concat([SourceEndpointAddressIP4, SourceEndpointAddressIP6])
| UserHash   := concat([SourceAccountUserName, SourceAccountAzureId])
| UserHash   := crypto:md5([UserHash])

// Handle unregistered devices
| case {
    SourceEndpointHostName="" | SourceEndpointHostName := "{Unregistered Device}";
    *
}

// Aggregate per user per login event
| groupBy([UserHash, ContextTimeStamp],
    function=[collect([SourceAccountUserName, SourceAccountAzureId, SourceIP,
                       SourceEndpointHostName, ISPDomain, ClientUserAgentString])], limit=max)

// Geo-enrich the source IP
| ipLocation(SourceIP)

// Retrieve previous login for same user
| neighbor([ContextTimeStamp, SourceIP, ISPDomain, UserHash,
            SourceIP.country, SourceIP.lat, SourceIP.lon], prefix=prev)
| test(UserHash == prev.UserHash)

// Calculate travel metrics
| LogonDelta    := (ContextTimeStamp - prev.ContextTimeStamp) * 1000
| LogonDelta    := round(LogonDelta)
| TimeToTravel  := formatDuration(LogonDelta, precision=2)
| DistanceKm    := (geography:distance(lat1="SourceIP.lat", lat2="prev.SourceIP.lat",
                    lon1="SourceIP.lon", lon2="prev.SourceIP.lon")) / 1000
| DistanceKm    := round(DistanceKm)
| SpeedKph      := DistanceKm / (LogonDelta / 1000 / 60 / 60)
| SpeedKph      := round(SpeedKph)

// Filter: impossible travel speed and cross-country
| test(SpeedKph > 900)
| test(SourceIP.country != prev.SourceIP.country)

// Format output
| Travel := format(format="%s → %s", field=[prev.SourceIP.country, SourceIP.country])
| table([SourceAccountUserName, Travel, TimeToTravel, DistanceKm, SpeedKph],
    sortby=DistanceKm, order=desc)
```

**Notes:**
- `neighbor()` returns the previous row for a sorted sequence — requires the dataset to be sorted by `ContextTimeStamp` within the `groupBy()`
- `crypto:md5()` anonymizes the user identifier for consistent hashing without exposing PII in intermediate results
- 900 km/h is roughly commercial aircraft speed — tune based on your organization's legitimate remote access patterns (e.g., VPN users may appear to teleport)
- Requires Identity Protection license and SSO event ingestion
- The `!cidr(... "0.0.0.0/16")` exclusion removes unresolvable or internal addresses from geo enrichment

---

*CQL Real-World Query Examples — ThreatHunter docs/cql-query-examples.md*
*Sources: ByteRay-Labs/Query-Hub; LogScale Documentation v1.229.0–1.232.0*
*For syntax reference, see: docs/cql-syntax.md*
