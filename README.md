# Azure DevOps Work Items Migration Scripts (stdlib-only)

A set of **Python scripts (stdlib only)** to copy / enrich Azure DevOps Work Items from a **source** project to a **target** project using Azure DevOps REST APIs.

This repo is intentionally **public-friendly**:
- no hardcoded org URLs
- no hardcoded project names
- no Personal Access Tokens (PATs) in code

## Configuration (required)

Use env vars (recommended):

- `ADO_SOURCE_ORG_URL` (e.g. `https://dev.azure.com/<sourceOrg>`)
- `ADO_SOURCE_PROJECT`
- `ADO_SOURCE_PAT`
- `ADO_TARGET_ORG_URL` (e.g. `https://dev.azure.com/<targetOrg>`)
- `ADO_TARGET_PROJECT`
- `ADO_TARGET_PAT`

Optional (attachments scripts):
- `ADO_ATTACHMENTS_DIR` (folder where attachments are stored)

## Scripts

- `scripts/copy_parent_workitems_with_children.py`  
  Copy parent work items, children (Hierarchy), Related links, optional comments.

- `scripts/copy_last_workbundles.py`  
  Copy the N most recently created "Work Bundle" items (or other types you configure).

- `scripts/copy_single_workitem.py`  
  Copy a single work item by ID.

- `scripts/diagnostic_fields.py`  
  Compare fields between source and target process templates for given work item types.

- `scripts/download_attachments.py`  
  Download attachments/images from source items mapped from target via `Custom.ReflectedWorkItemId`.

- `scripts/upload_attachments.py`  
  Upload local attachments to target and attach them to mapped work items.

- `scripts/link_workbundles_related.py`  
  Link existing work items to Work Bundles in the target based on mappings (configurable).

## Quick start

PowerShell:

```powershell
$env:ADO_SOURCE_ORG_URL="https://dev.azure.com/sourceOrg"
$env:ADO_SOURCE_PROJECT="SourceProject"
$env:ADO_SOURCE_PAT="..."

$env:ADO_TARGET_ORG_URL="https://dev.azure.com/targetOrg"
$env:ADO_TARGET_PROJECT="TargetProject"
$env:ADO_TARGET_PAT="..."

python scripts/copy_parent_workitems_with_children.py --max 10 --with-comments
```

Linux/macOS:

```bash
export ADO_SOURCE_ORG_URL="https://dev.azure.com/sourceOrg"
export ADO_SOURCE_PROJECT="SourceProject"
export ADO_SOURCE_PAT="..."

export ADO_TARGET_ORG_URL="https://dev.azure.com/targetOrg"
export ADO_TARGET_PROJECT="TargetProject"
export ADO_TARGET_PAT="..."

python scripts/copy_parent_workitems_with_children.py --max 10
```

## Security

Never commit PATs or `.env` files. If a PAT was ever committed to any repo, revoke and re-create it.

