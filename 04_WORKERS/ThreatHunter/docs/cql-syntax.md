# CrowdStrike Query Language (CQL) — Syntax Reference
### ThreatHunter Knowledge Base | docs/cql-syntax.md

> **Sources:** CrowdStrike LogScale Skill (built-in); LogScale Documentation v1.229.0–1.232.0 (library.humio.com); ByteRay-Labs/Query-Hub (github.com)
> **Last updated:** 2026-03-23 (v1.1 — added operator precedence fix, `like`/`<=>` operators, `=~` detail, eval expressions, user parameters, saved searches, relative time syntax, regex engine V1/V2 reference, new event types and fields)
> **See also:** [Query Language Syntax — LogScale Docs](https://library.humio.com/data-analysis/syntax.html) | [CQL Grammar Subset](https://library.humio.com/lql-grammar/syntax-grammar-guide.html)

---

## Table of Contents

1. [Pipeline Architecture](#1-pipeline-architecture)
2. [Comments](#2-comments)
3. [Filter Operators](#3-filter-operators)
4. [Logical Operators & Precedence](#4-logical-operators--precedence)
5. [Wildcards and Patterns](#5-wildcards-and-patterns)
6. [Free-Text Filters](#6-free-text-filters)
7. [Regex](#7-regex)
8. [Field Assignment and Expressions](#8-field-assignment-and-expressions)
9. [User Parameters / Variables](#9-user-parameters--variables)
10. [Saved Searches (User Functions)](#10-saved-searches-user-functions)
11. [Essential Functions](#11-essential-functions)
12. [Conditional Logic](#12-conditional-logic)
13. [Join Operations](#13-join-operations)
14. [Array Operations](#14-array-operations)
15. [Common Falcon Event Types](#15-common-falcon-event-types)
16. [Common Field Names](#16-common-field-names)
17. [Detection Query Templates (ATT&CK-Mapped)](#17-detection-query-templates-attck-mapped)
18. [Performance Guide](#18-performance-guide)
19. [Well-Known SIDs](#19-well-known-sids)
20. [Troubleshooting](#20-troubleshooting)

---

## 1. Pipeline Architecture

CQL uses Unix-style pipes. Each expression passes its output to the next stage. Filters narrow the event set; functions transform or aggregate it.

```
#event_simpleName = ProcessRollup2
| CommandLine = *powershell*
| groupBy(ComputerName, function=count())
| sort(_count, order=desc)
```

**Key rules:**
- Tag filters (`#field`) are always fastest — put them first
- Free-text search is only valid **before** the first aggregate function
- Pipe `|` separates stages; space between filters is an implicit AND

---

## 2. Comments

```
// Single-line comment

/* Multi-line
   comment */
```

---

## 3. Filter Operators

| Operator | Usage | Example |
|---|---|---|
| `=` | Exact match | `status = 200` |
| `!=` | Not equal | `status != 404` |
| `=~` | Apply a function to a field (field operator) | `ip =~ cidr(subnet="10.0.0.0/8")` |
| `:=` | Field assignment (create/overwrite) | `newField := "value"` |
| `<` `>` `<=` `>=` | Numeric comparison | `responseTime > 1000` |
| `= *glob*` | Wildcard match | `CommandLine = *mimikatz*` |
| `= /regex/` | Regex match | `UserName = /admin.*/i` |
| `like` | Contains string (case-sensitive); equivalent to `= *value*` | `class like "Bucket"` |
| `<=>` | Link operator — maps field relationships inside `correlate()` | `correlate(...)` |

### The `=~` Field Operator

`=~` is shorthand for passing a field to any function that accepts a `field=` parameter:

```
// These are equivalent:
| ip_addr =~ cidr(subnet="10.0.0.0/8")
| cidr(subnet="10.0.0.0/8", field=ip_addr)

// Also works with regex(), replace(), and others:
| url =~ regex("login")
| url =~ replace(regex=/http/, with="https")
```

### The `like` Operator

`like` provides readable contains/pattern matching:

```
class like "Bucket"        // Contains "Bucket" (case-sensitive)
class like "foo*bar"       // Starts with foo, ends with bar
class = /Bucket/           // Equivalent regex form
```

---

## 4. Logical Operators & Precedence

```
// OR — use lowercase 'or'
status = 200 or status = 201

// AND — implicit (space) or explicit keyword
method = GET status = 200       // Implicit AND
method = GET AND status = 200   // Explicit AND

// NOT — use 'not', '!', or '!=' prefix
status != 404
!in(status, values=[400, 401, 403])
NOT LocalIP = "192.168.1.10"

// Grouping with parentheses
(status = 200 or status = 201) method = GET
```

> ⚠️ **Critical — CQL precedence is opposite to most languages:**
> **`NOT` > `OR` > `AND`** — OR binds *closer* than AND.

```
foo and not bar or baz    // → foo and ((not bar) or baz)
foo or not bar and baz    // → (foo or (not bar)) and baz
```

**Always use parentheses when mixing AND and OR** to avoid subtle bugs from this counter-intuitive precedence order.

### Negating Filter Functions

```
| !cidr(ip, subnet="127.0.0/16")
| !in(field, values=[a, b, c])
| !regex("pattern")
```

---

## 5. Wildcards and Patterns

```
field = *value*        // Contains
field = value*         // Starts with
field = *value         // Ends with
field = *              // Field exists (is non-empty)
field != *             // Field does not exist
field = ""             // Field is empty string
```

---

## 6. Free-Text Filters

Free-text searches across all fields except special fields (`@id`, `@timestamp`, `@ingesttimestamp`, tag fields):

```
"error message"        // Exact phrase across all fields
error                  // Single word across all fields
/192\.168\.1\.\d+/     // Regex across all fields — SLOW, avoid in production
```

**Critical limitations:**
- Free-text is only valid **before** the first aggregate function (e.g., `groupBy`, `count`)
- Does not search fields added or modified within the pipeline
- Use `@rawstring = "text"` for explicit raw event search
- **Always prefer field-specific filters** (`field = value`) over free-text for performance

---

## 7. Regex

### Inline vs. Function Syntax

| Syntax | Scope | Performance | Use When |
|---|---|---|---|
| `field = /pattern/` | Single field | Fast | Simple field matching |
| `/pattern/` | All fields | Slow | Quick exploration only — not production |
| `regex("pattern", field=f)` | Specified field | Fast | Need `strict`, `repeat`, or named capture groups |

```
// Preferred — targets specific field
| CommandLine = /mimikatz/i

// Preferred — function with named group extraction
| regex("(?<user>\\w+)@(?<domain>\\w+)", field=email, strict=false)

// Avoid in production — searches all fields
| /mimikatz/
```

### Regex Flags

| Flag | Meaning |
|---|---|
| `i` | Case-insensitive |
| `m` | Multiline (`^` and `$` match line starts/ends) — default in `regex()` |
| `d` / `s` | Dotall — `.` matches any character including newline |
| `g` | Global — match expression multiple times within a single event |
| `F` | Use Regex Engine V2 (default from v1.227) |

```
// Apply flags inline:
/orgname/i
/(?i)orgname/
/(?i:orgname)extension/

// Apply flags in regex() function:
| regex("orgname", flags="i")
```

### Regex Engine V1 vs V2

V2 is the default from LogScale v1.227 (enabled via `F` flag in earlier versions). Key behavioral differences:

| Behaviour | V1 (JitRex) | V2 |
|---|---|---|
| `\h` | Literal `h` | Horizontal whitespace |
| `\v` | Literal `v` | Vertical whitespace |
| `\b` | Unicode word boundary | ASCII word boundary |
| `\W` | `[^a-zA-Z]` | `[^a-zA-Z_0-9]` |
| In-line flags | Apply to first branch only | Apply to entire alternation |

> Use `regex("pattern", repeat=true)` for multiple matches — NOT the `/g` flag. `regex()` does not support `/g`.

### Named Capture Groups

Named groups in regex automatically create new fields:

```
| regex("(?<srcIP>\\d+\\.\\d+\\.\\d+\\.\\d+):(?<srcPort>\\d+)", field=ConnectionInfo)
// Creates fields: srcIP, srcPort
```

---

## 8. Field Assignment and Expressions

### `:=` Assignment

```
// Create or overwrite a field
newField := "static value"
newField := existingField
newField := format("%s-%s", field1, field2)

// Shorthand for functions with 'as' parameter
| foo := min(x)        // same as: min(x, as=foo)
| bar := max(x)        // same as: max(x, as=bar)

// Using 'as' directly inside functions
| count(as=totalCount)
| avg(responseTime, as=avgResponse)
```

### `eval()` and Expression Arithmetic

`eval()` and `:=` both support arithmetic expressions. All values are strings interpreted in context:

```
| foo := a + b
| bar := a / b
// equivalent to:
| eval(foo = a + b) | eval(bar = a / b)

// Real-world rate calculation example:
| firstLastDeltaHours := ((LastAttempt - FirstAttempt) / 60 / 60)
| attemptsPerHour := (failCount / firstLastDeltaHours)
```

### Expression Operators

| Type | Operators | Note |
|---|---|---|
| Arithmetic | `+`, `-`, `/`, `*`, `%` | Operates on numeric strings |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` | Use `==` in expressions (not `=`, which is a filter) |
| Logical negation | `!` | |

> **Note:** `a = b` is a **field filter**, not a comparison. Use `==` inside `test()`, `eval()`, and `:=` expressions. There are no logical AND/OR operators inside expressions — use `test()` with those.

---

## 9. User Parameters / Variables

Create user-supplied parameters with a `?` prefix. Useful for building reusable saved searches and dashboard widgets:

```
matchstring := ?searchtext
matchstring := ?"Matching String to Locate"
```

### Default Values (for triggers and scheduled searches)

```
?{PARAMETER=VALUE}
?{basefield="@host"}
```

> **Note:** Default values only work in saved searches. Dashboards use `*` by default.

### Using Parameters in Saved Searches

```
// Saved search defined as:
groupBy(field=?{basefield="@host"})

// Called with:
$grouped(basefield="@host")
```

### Multi-Value Parameters

For dashboards, use commas as delimiters in user input:

```
cat, hat        // Two individual values
"cat, hat"      // Single value containing a comma
```

---

## 10. Saved Searches (User Functions)

Saved searches act as reusable query functions. Call them with `$` prefix:

```
$"SAVED_QUERY_NAME"()
$nameOfSavedQuery()
$"My Saved Query"() | $filterOutFalsePositive() | ...
```

### Arguments

Define parameters with `?argname` in the saved query body:

```
// Saved as "findhost":
host = ?host

// Called with:
$findhost(host="gendarme")
```

### Multi-Valued Arguments (v1.140+)

```
$mySavedQuery(mvArgument=["value1", "value2", "value3"])
// used in the saved query body as:
in(values=?mvArgument, field=argument)
```

### Using Saved Searches as Function Arguments

```
groupBy("myField", function=[count(), {id=42 | $"My Saved Query"()}])
```

### Referencing Resources

```
$parser://myParser()                    // Reference a parser
$parser://package/scope:myParser()      // Scoped parser
$query://myQuery()                      // Reference a saved query explicitly
```

---

## 11. Essential Functions

### Aggregation

```
count()                                    // Count all events
count(field)                               // Count non-null values of a field
count(field, distinct=true)                // Count unique values (distinct count)
sum(field)                                 // Sum numeric field
avg(field)                                 // Average
min(field) / max(field)                    // Min / Max
percentile(field, percentiles=[50,95,99])  // Percentile distribution
stdDev(field)                              // Standard deviation
```

### Grouping, Sorting, and Limiting

```
// Group by one field
| groupBy(UserName, function=count())

// Group by multiple fields with multiple aggregations
| groupBy([UserName, ComputerName], function=[count(), collect(CommandLine)])

// Sort
| sort(field, order=desc, limit=100)
| sort(_count, order=desc)

// Top N values
| top(field, limit=10)

// Limit output
| head(10)      // First N events
| tail(10)      // Last N events
```

### Filtering Functions

```
// in() — match against a list of values
| in(status, values=[200, 201, 204])
| in(status, values=["error", "warning"], ignoreCase=true)
| !in(status, values=[400, 401])          // Negation

// test() — complex conditional expression
| test(field1 > field2)
| test(responseTime > 1000 AND status != 200)

// cidr() — IP subnet matching
| cidr(sourceIP, subnet="10.0.0.0/8")

// regex() — pattern matching with extraction
| regex("(?<user>\\w+)@(?<domain>\\w+)", field=email)
```

### String Functions

```
| lower(field)                                    // Lowercase
| upper(field)                                    // Uppercase
| concat([field1, field2])                        // Concatenate
| format("%s: %d", name, count)                   // Format string
| replace(field, regex=/old/, with="new")         // Regex replace
| length(field)                                   // String length
| split(field, by=",")                            // Split to array
| splitString(field, by=":", index=0)             // Get specific part by index
```

### Time Functions

```
| formatTime("%Y-%m-%d %H:%M:%S", field=@timestamp, as=readableTime)
| formatTime(format="%F %T.%L", field=ContextTimeStamp)   // Full datetime with ms
| parseTimestamp("yyyy-MM-dd", field=dateString)
| bucket(span=1h)                                          // Bucket events into time windows
| timeChart(span=5m, function=count())                     // Time series chart

// Extract time components
| time:hour(field=@timestamp, as=hour)
| time:dayOfWeek(field=@timestamp, as=dow)

// Rate unit conversion in timeChart:
| timeChart(function=sum(bytes), unit="bytes/span to Mi bytes/day")
| timeChart(function=sum(bytes), unit="bytes/sec to Mibytes/day")
```

### Relative Time Syntax

Use duration strings when specifying time ranges or `span=` values:

| Full form | Abbreviations |
|---|---|
| `millisecond(s)` | `millis`, `ms` |
| `second(s)` | `s`, `sec`, `secs` |
| `minute(s)` | `m`, `min` |
| `hour(s)` | `h`, `hr`, `hrs` |
| `day(s)` | `d` |
| `week(s)` | `w` |
| `month(s)` | `mon` |
| `quarter(s)` | `q`, `qtr`, `qtrs` |
| `year(s)` | `y`, `yr`, `yrs` |

**Examples:** `2h`, `2 hours`, `3 weeks`, `10s`, `30m`

### Calendar-Based Units

Prefix with `calendar:` for calendar-aware interpretation instead of fixed duration:

```
calendar: 2months   // May 24 → March 24 (calendar months back)
2months             // May 24 → March 25 (60 fixed days back)
```

### Anchoring with `@`

Snap relative times to specific time boundaries using `@`:

```
1d@d+12h      // "Yesterday at 12 PM"
              // 1. Go back 1 day
              // 2. Snap (@d) to start of that day (00:00)
              // 3. Add 12 hours
```

| Syntax | Meaning |
|---|---|
| `now@d` | Start of today |
| `now@w` | Start of this week |
| `calendar:1d@d` | Start of yesterday (calendar) |
| `now@quarter` | Start of current quarter |
| `6h@h+30min` | 6 hours ago, snapped to hour, plus 30 min |

> **Limitation:** Calendar-based units and anchoring (`@`) are NOT supported in live queries, scheduled searches, or as `span=` values in `timeChart()`/`bucket()`.

### Data Manipulation

```
| rename(oldField, as=newField)
| drop([field1, field2])            // Remove fields from output
| select([field1, field2])          // Keep only specified fields
| table([field1, field2, field3])   // Display as formatted table
| default(field, value="N/A")       // Set default if field is null/missing
| coalesce([field1, field2])        // Return first non-null value
```

### Parsing Functions

```
| parseJson(field=rawJson)          // Parse JSON string into fields
| kvParse()                         // Parse key=value pairs
| parseCsv(field=csvData)           // Parse CSV
| parseUrl(field=url)               // Extract URL components (host, path, query)
| base64Decode(field=encoded)       // Decode base64
```

---

## 12. Conditional Logic

### case Statement

Evaluates conditions in order; first match wins. Use `*` as a catch-all default:

```
| case {
    status < 300 | category := "success";
    status < 400 | category := "redirect";
    status < 500 | category := "client_error";
    * | category := "server_error";
}
```

### match Statement

Match a single field against patterns or values:

```
| match(status) {
    200 => result := "OK";
    404 => result := "Not Found";
    /5\d\d/ => result := "Server Error";
    * => result := "Unknown";
}
```

### if() Function

```
| if(status < 400, then="success", else="error", as=result)
| eval(severity = if(score > 80, "critical", if(score > 50, "high", "low")))
```

---

## 13. Join Operations

### join() — Cross-Query Join

Links results from a sub-query to the main query on a shared key field:

```
| join({
    #event_simpleName = UserLogon
    | rename(UserName, as=joinUser)
}, field=UserSid, key=UserSid)
```

### selfJoin() — Same-Dataset Correlation

Joins events from the same dataset where two conditions are met for the same key:

```
| selfJoin(field=[SessionId], where=[
    {#event_simpleName=ProcessRollup2},
    {#event_simpleName=NetworkConnect}
])
```

### selfJoinFilter() — Correlated Event Analysis

Links process execution with related network/DNS activity by process ID and agent ID:

```
#event_simpleName = /ProcessRollup2|DnsRequest/
| falconPID := ContextProcessId
| falconPID := TargetProcessId
| selfJoinFilter(field=[aid, falconPID], where=[
    {#event_simpleName = /ProcessRollup2/},
    {#event_simpleName = /DnsRequest/}
])
| groupBy([aid, ComputerName, falconPID], function=collect([FileName, DomainName, CommandLine]))
```

### Process-to-Network Correlation Pattern

```
#event_simpleName = NetworkConnectIP4
| RemoteAddressIP4 != "10.*" RemoteAddressIP4 != "192.168.*"
| rename(field=ContextProcessId_decimal, as=TargetProcessId_decimal)
| join(query={#event_simpleName = ProcessRollup2}, field=TargetProcessId_decimal)
| table([ComputerName, ImageFileName, RemoteAddressIP4, RemotePort, CommandLine])
```

### Lookup Files

```
| match(file="threat_intel.csv", field=SHA256Hash, column=hash)
| readFile("users.csv")
```

---

## 14. Array Operations

```
| array:contains(field[], value="target")       // True if array contains value
| array:length(items[])                         // Count array elements
| array:filter(items[], var=x, condition=test(x > 10))  // Filter array elements
```

---

## 15. Common Falcon Event Types

### Process Events

| Event | Description |
|---|---|
| `ProcessRollup2` | Process execution — full details including command line, parent, hash |
| `SyntheticProcessRollup2` | Enriched process data |
| `ProcessBlocked` | Process execution blocked by policy |
| `ScriptControlScan` | Script execution monitoring |
| `NewExecutableWritten` | New executable written to disk |
| `NewExecutableRenamed` | Executable renamed (masquerading detection) |
| `ExecutableDeleted` | Executable deleted |

### Network Events

| Event | Description |
|---|---|
| `NetworkConnectIP4` | IPv4 outbound/inbound connections |
| `NetworkConnectIP6` | IPv6 connections |
| `DnsRequest` | DNS queries made by processes |
| `HttpRequest` | HTTP traffic (requires enablement) |

### Authentication Events

| Event | Description |
|---|---|
| `UserLogon` | Successful user logon |
| `UserLogoff` | User logoff |
| `UserLogonFailed2` | Failed logon attempt |

### Active Directory / Identity Events (requires Identity Protection license)

| Event | Description |
|---|---|
| `ActiveDirectoryAccountLocked` | Account lockout event |
| `ActiveDirectoryAuthenticationFailure` | Failed AD authentication |
| `ActiveDirectoryAccountCreated` | New AD account created |
| `ActiveDirectoryAccountDirectContainingGroupEntitiesUpdate` | Group membership change |
| `ActiveDirectoryAccountPasswordUpdate` | Password changed |
| `UserAccountAddedToGroup` | User added to a group |

### File Events

| Event | Description |
|---|---|
| `RansomwareOpenFile` | Ransomware behavior indicator |
| `FileWritten` | File write event (use with `#event_simpleName=/FileWritten$/`) |

### Scheduled Task Events

| Event | Description |
|---|---|
| `ScheduledTaskRegistered` | New scheduled task registered (supports `parseXml(TaskXml)`) |

### SSO / Cloud Identity Events (requires Identity Protection license)

| Event | Description |
|---|---|
| `SsoApplicationAccess` | SSO application access event |
| `SsoUserLogon` | SSO user logon |
| `UserIdentity` | User identity context — enrichment event joinable on `AuthenticationID` |

---

## 16. Common Field Names

### Process Fields

| Field | Description |
|---|---|
| `ImageFileName` | Full path of process executable |
| `CommandLine` | Full command line including arguments |
| `ParentBaseFileName` | Parent process executable name |
| `SHA256HashData` | SHA-256 hash of the executable |
| `UserSid` | User SID |
| `UserName` | Username running the process |
| `ComputerName` | Hostname |
| `TargetProcessId` | Process ID (hex) |
| `TargetProcessId_decimal` | Process ID (decimal) |
| `ContextProcessId` | Context process ID (for child events) |
| `ContextProcessId_decimal` | Context process ID (decimal) |
| `aid` | Agent ID — unique sensor identifier |

### Network Fields

| Field | Description |
|---|---|
| `RemoteAddressIP4` | Remote IPv4 address |
| `RemotePort` | Remote port |
| `LocalAddressIP4` | Local IPv4 address |
| `LocalPort` | Local port |
| `ContextBaseFileName` | Process making the connection |

### Authentication / Identity Fields

| Field | Description |
|---|---|
| `SamAccountName` | AD sAMAccountName (username) |
| `AccountDomain` | AD domain |
| `AuthenticationID` | Authentication ID — join key between `ProcessRollup2` and `UserIdentity` |
| `SourceEndpointHostName` | Source machine hostname |
| `SourceEndpointIp` | Source IP address |
| `SourceEndpointAddressIP4` | IPv4 address for SSO/identity events |
| `SourceEndpointAddressIP6` | IPv6 address for SSO/identity events |
| `SourceAccountUserName` | Username in SSO/cloud identity events |
| `SourceAccountAzureId` | Azure user object ID |
| `ISPDomain` | ISP domain from geo-enriched identity events |
| `FailureReason` | Authentication failure reason |
| `LogonType` | Logon type code (e.g., 10 = remote interactive) |
| `SubStatus` | Logon sub-status code (NTSTATUS) — convert to hex for readability |
| `ContextTimeStamp` | Event timestamp in epoch format (convert with `formatTime()`) |

### Registry Fields

| Field | Description |
|---|---|
| `RegObjectName` | Registry key path |
| `RegValueName` | Registry value name |
| `RegStringValue` | Registry value data (string) |

---

## 17. Detection Query Templates (ATT&CK-Mapped)

### T1547.001 — Registry Run Key Persistence
```
#event_simpleName = /AsepValueUpdate|RegGenericValueUpdate/
| platform = Win
| RegObjectName = /\\Software\\Microsoft\\Windows\\CurrentVersion\\Run/i
| groupBy([ComputerName, RegObjectName, RegValueName], function=count())
```

### T1059.001 — Encoded PowerShell
```
#event_simpleName = ProcessRollup2
| ImageFileName = /powershell\.exe$/i
| CommandLine = /(-enc\s|-encodedcommand\s|-e\s+[A-Za-z0-9+\/=]{20,})/i
| table([@timestamp, ComputerName, UserName, CommandLine])
| sort(@timestamp, order=desc)
```

### T1566 — Office Process Spawning Suspicious Child
```
#event_simpleName = ProcessRollup2
| ParentBaseFileName = /(winword|excel|powerpnt|outlook)\.exe/i
| ImageFileName = /(cmd|powershell|wscript|cscript|mshta|certutil|bitsadmin)\.exe/i
| table([@timestamp, ComputerName, ParentBaseFileName, ImageFileName, CommandLine])
```

### T1218 — LOLBins with DNS Activity
```
#event_simpleName = DnsRequest
| rename(field=ContextProcessId_decimal, as=TargetProcessId_decimal)
| join(query={
    #event_simpleName = /ProcessRollup2/
    | FileName = /powershell\.exe|certutil\.exe|regsvr32\.exe|rundll32\.exe|bitsadmin\.exe|mshta\.exe/i
}, field=TargetProcessId_decimal)
| table([ComputerName, ImageFileName, DomainName, CommandLine])
```

### T1036.003 — Renamed Executable (Masquerading)
```
#event_simpleName = NewExecutableRenamed
| rename(field=TargetFileName, as=ImageFileName)
| join(query={#event_simpleName = /ProcessRollup2/}, field=[ImageFileName])
| table([aid, ComputerName, SourceFileName, ImageFileName, CommandLine])
```

### T1055 — In-Memory .NET Assembly (Suspicious DLL Load)
```
#event_simpleName = ImageHash
| rename(field=[[FileName, Dll_Loaded], [FilePath, Dll_Path]])
| selfJoinFilter(field=[aid, TargetProcessId], where=[
    {#event_simpleName = /ProcessRollup2/i},
    {FileName != /powershell\.exe/i},
    {#event_simpleName = ImageHash}
])
| in(field=Dll_Loaded, values=["mscoree.dll", "clr.dll", "clrjit.dll", "mscorlib.ni.dll"], ignoreCase=true)
| groupBy([aid, ComputerName, TargetProcessId], function=collect([FileName, CommandLine, Dll_Loaded]))
```

### T1021.001 — Lateral Movement via RDP
```
#event_simpleName = UserLogon
| LogonType = 10
| groupBy([ComputerName, UserName, RemoteAddressIP4], function=count())
| sort(_count, order=desc)
```

### T1110 — Account Lockout / Brute Force
```
#event_simpleName = ActiveDirectoryAccountLocked
| groupBy([SamAccountName, AccountDomain], function=[
    count(),
    collect(SourceEndpointHostName, limit=10)
])
| sort(_count, order=desc)
```

### T1078 — Privileged Group Membership Change
```
#event_simpleName = ActiveDirectoryAccountDirectContainingGroupEntitiesUpdate
| ActiveDirectoryDirectGroupObjectGuidsBuffer = *512*
   or ActiveDirectoryDirectGroupObjectGuidsBuffer = *519*
| table([@timestamp, SamAccountName, AccountDomain])
```

### User Added to Group (with SID Parsing)
```
#event_simpleName = UserAccountAddedToGroup
| parseInt(GroupRid, as=GroupRid, radix=16, endian=big)
| parseInt(UserRid, as=UserRid, radix=16, endian=big)
| UserSid := format(format="%s-%s", field=[DomainSid, UserRid])
| groupBy([aid, UserSid], function=[
    selectFromMin(field=@timestamp, include=[ComputerName]),
    collect([DomainSid, UserRid])
])
```

---

## 18. Performance Guide

### Recommended Filter Order (Fastest First)

1. **Tag filters** — `#event_simpleName = ProcessRollup2` (indexed; always first)
2. **Exact field matches** — `status = 200`
3. **Wildcard field matches** — `CommandLine = *mimikatz*`
4. **Field regex** — `UserName = /admin.*/i`
5. **`regex()` function** — `regex("pattern", field=CommandLine)`
6. **Free-text / all-field regex** — `/error/` (avoid in production)

### Filter Performance at a Glance

| Filter Type | Example | Speed |
|---|---|---|
| Tag filter | `#event_simpleName = ProcessRollup2` | Fastest |
| Exact field match | `status = 200` | Fast |
| Field wildcard | `CommandLine = *mimikatz*` | Medium |
| Field regex | `UserName = /admin.*/i` | Medium |
| `regex()` function | `regex("pattern", field=CommandLine)` | Medium |
| All-field regex | `/error/` | Slow |
| Free-text | `"error message"` | Slowest |

### Key Rules

- **Free-text only before aggregates** — `"text"` after `groupBy()` is invalid
- **Always target a field in regex** — `field = /pattern/` is significantly faster than `/pattern/` alone
- **Use `@rawstring` explicitly** when you must search raw events: `@rawstring = /pattern/`
- **Never use `*` alone** — returns everything and is extremely expensive
- **Add `| head(1000)` while developing** — limit result sets before finalizing queries
- **Implicit AND** — filters separated by a space are ANDed: `status = 200 method = GET`

### Special Fields Not Searched by Free-Text

- `@id` — Event ID
- `@timestamp` — Event timestamp
- `@ingesttimestamp` — Ingestion time
- All tag fields (prefixed with `#`)

---

## 19. Well-Known SIDs

| SID Suffix | Group |
|---|---|
| `-512` | Domain Admins |
| `-519` | Enterprise Admins |
| `-518` | Schema Admins |
| `-544` | Administrators (local) |
| `-500` | Built-in Administrator account |
| `-501` | Guest account |

Use these when hunting for privileged group membership changes or suspicious account activity targeting high-value groups.

---

## 20. Troubleshooting

**No results returned:**
1. Check the UI time range — it may be too narrow
2. Run `*` alone to confirm data exists in the repository
3. Run `* | groupBy(#event_simpleName)` to see what event types are available
4. Check the repository selector — ensure you're querying the right data source
5. Identity Protection events (`ActiveDirectory*`) require the Identity Protection license and ingestion

**Query is slow:**
1. Add `#event_simpleName` as the first filter
2. Move all field-specific filters as early in the pipeline as possible
3. Reduce the time range
4. Replace free-text or all-field regex with field-specific alternatives
5. Add `| head(1000)` during development to limit evaluation

**Regex not matching expected values:**
1. Check for case sensitivity — add `i` flag: `/pattern/i`
2. Escape special regex characters: `.` `*` `+` `?` `(` `)` `[` `]` `{` `}` `\` `^` `$` `|`
3. Use `strict=false` in `regex()` to avoid dropping events with no match
4. Test with a simple exact match first to confirm the field contains what you expect

---

*CrowdStrike Query Language Syntax Reference — ThreatHunter docs/cql-syntax.md | v1.1*
*Sources: CrowdStrike LogScale Skill; LogScale Documentation v1.229.0–1.232.0; ByteRay-Labs/Query-Hub*
*For the full function library, see: https://library.humio.com/data-analysis/syntax.html*
*For real-world query examples, see: docs/cql-query-examples.md*
