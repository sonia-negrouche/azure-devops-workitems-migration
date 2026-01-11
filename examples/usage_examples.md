# Usage examples

This document provides common usage examples for the Azure DevOps work items migration scripts.

All scripts rely on **environment variables** for configuration.
You can also pass values explicitly via CLI arguments.

---

## Environment variables

Required for most scripts:

- `ADO_SOURCE_ORG_URL`
- `ADO_SOURCE_PROJECT`
- `ADO_SOURCE_PAT`
- `ADO_TARGET_ORG_URL`
- `ADO_TARGET_PROJECT`
- `ADO_TARGET_PAT`

Optional:
- `ADO_ATTACHMENTS_DIR` (for attachments scripts)

---

## PowerShell examples (Windows)

### Configure environment

```powershell
$env:ADO_SOURCE_ORG_URL="https://dev.azure.com/sourceOrg"
$env:ADO_SOURCE_PROJECT="SourceProject"
$env:ADO_SOURCE_PAT="xxxxx"

$env:ADO_TARGET_ORG_URL="https://dev.azure.com/targetOrg"
$env:ADO_TARGET_PROJECT="TargetProject"
$env:ADO_TARGET_PAT="yyyyy"

$env:ADO_ATTACHMENTS_DIR="C:\temp\ado_attachments"
