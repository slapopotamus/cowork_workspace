# Security Standard Operating Procedures
**Version:** 1.0 (Scaffold) | **Effective:** 2026-03-19
**Owner:** Hootz — Cybersecurity Operations Chief of Staff
**Status:** PLACEHOLDER — Sections to be populated as work begins.

---

## Table of Contents
1. [PowerShell Scripting Standards](#1-powershell-scripting-standards)
2. [CrowdStrike Audit Checklists](#2-crowdstrike-audit-checklists)
3. [Query Development Standards](#3-query-development-standards) *(placeholder)*
4. [Incident Response Runbooks](#4-incident-response-runbooks) *(placeholder)*
5. [Output and Reporting Standards](#5-output-and-reporting-standards) *(placeholder)*

---

## 1. PowerShell Scripting Standards

### 1.1 Required Script Header
Every PowerShell script produced in this workspace must include the following header block:

```powershell
<#
.SYNOPSIS
    [One-line description of what the script does.]
.DESCRIPTION
    [Detailed description. Include purpose, scope, and any dependencies.]
.PARAMETER ParameterName
    [Description of each parameter.]
.EXAMPLE
    [At least one usage example with expected output noted.]
.NOTES
    Author      : Hootz / [Analyst Name]
    Version     : 1.0
    Created     : YYYY-MM-DD
    Modified    : YYYY-MM-DD
    Environment : [Target environment — e.g., CrowdStrike RTR, Domain Controller, etc.]
    References  : [Links to relevant docs, KB articles, or threat intel.]
#>
```

### 1.2 Error Handling Requirements
All scripts must implement structured error handling. Minimum standard:

```powershell
try {
    # Primary logic block
} catch [System.SpecificException] {
    Write-Error "Specific error: $_"
    # Targeted remediation or graceful exit
} catch {
    Write-Error "Unhandled exception in [FunctionName]: $_"
    exit 1
} finally {
    # Cleanup — close connections, remove temp files, flush logs
}
```

- **No bare `catch {}` blocks.** Every catch must log or surface the error.
- Use `$ErrorActionPreference = 'Stop'` at the top of scripts unless selective error handling is required.
- Exit codes must be meaningful: `0` = success, `1` = general failure, `2+` = specific error conditions (document these in the header).

### 1.3 Logging Requirements
All scripts that run unattended or touch production systems must implement logging:

```powershell
function Write-Log {
    param(
        [string]$Message,
        [ValidateSet('INFO','WARN','ERROR','DEBUG')]
        [string]$Level = 'INFO'
    )
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $entry = "[$timestamp] [$Level] $Message"
    Write-Output $entry
    Add-Content -Path $LogPath -Value $entry
}
```

- Log file path must be a defined parameter with a sensible default.
- Log rotation or size limits must be considered for long-running scripts.
- Sensitive values (passwords, tokens, hashes of sensitive data) must **never** be written to logs.

### 1.4 Security-Specific Requirements
- **No hardcoded credentials.** Use `Get-Credential`, environment variables, or a secrets manager.
- **Principle of least privilege.** Scripts must request only the permissions required.
- **Input validation.** All external input must be validated before use — especially in RTR scripts where input originates from a remote host.
- **Execution Policy.** Do not bypass execution policy in production. Scripts should be properly signed.

### 1.5 Code Review Checklist (Pre-Deployment)
- [ ] Header block complete and accurate
- [ ] Error handling implemented per 1.2
- [ ] Logging implemented per 1.3
- [ ] No hardcoded credentials or sensitive values
- [ ] Input validation present where applicable
- [ ] Tested in non-production environment
- [ ] Output verified against expected results
- [ ] Script reviewed by second analyst for high-impact operations

---

## 2. CrowdStrike Audit Checklists

> **STATUS: PLACEHOLDER** — Checklists to be developed and populated as audit work begins.

### 2.1 Sensor Coverage Audit
*To be defined. Checklist items will cover: sensor deployment gaps, stale sensors, version currency, RFM status.*

- [ ] *(Placeholder)*

### 2.2 Detection Policy Audit
*To be defined. Will cover: prevention policy configuration, detection thresholds, exclusion review.*

- [ ] *(Placeholder)*

### 2.3 Response Policy Audit
*To be defined. Will cover: RTR policy scope, approved responders, command restrictions.*

- [ ] *(Placeholder)*

### 2.4 Identity Protection Audit
*To be defined. Will cover: Falcon Identity Protection configuration, monitored accounts, alert thresholds.*

- [ ] *(Placeholder)*

### 2.5 Threat Hunting Review
*To be defined. Will cover: saved searches, scheduled queries, dashboard hygiene, alert fatigue indicators.*

- [ ] *(Placeholder)*

---

## 3. Query Development Standards
*(Placeholder — to be populated. Will cover: CQL/KQL/SPL style guide, performance standards, peer review requirements, naming conventions for saved queries.)*

---

## 4. Incident Response Runbooks
*(Placeholder — to be populated. Will cover: escalation paths, evidence collection procedures, communication templates, containment decision criteria.)*

---

## 5. Output and Reporting Standards
*(Placeholder — to be populated. Will cover: report templates, classification markings, distribution rules, executive vs. technical summary formats.)*

---

*This document is a living SOP. Update version number and `Modified` date with each substantive change.*
