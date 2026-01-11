#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: post a comment to a target work item (as System.History patch).

Required env/args:
  ADO_TARGET_ORG_URL, ADO_TARGET_PROJECT, ADO_TARGET_PAT
Usage:
  python examples/test_post_comment.py --id 12345 --text "hello"
"""
from __future__ import annotations

import argparse
import sys

from scripts._common import API_VERSION, AdoConn, env, require, http_json


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-org", default=env("ADO_TARGET_ORG_URL"))
    ap.add_argument("--target-project", default=env("ADO_TARGET_PROJECT"))
    ap.add_argument("--target-pat", default=env("ADO_TARGET_PAT"))
    ap.add_argument("--id", type=int, required=True)
    ap.add_argument("--text", required=True)
    return ap.parse_args()


def main():
    a = parse_args()
    tgt = AdoConn(require(a.target_org,"target_org","ADO_TARGET_ORG_URL"),
                 require(a.target_project,"target_project","ADO_TARGET_PROJECT"),
                 require(a.target_pat,"target_pat","ADO_TARGET_PAT"))

    patch = [{"op": "add", "path": "/fields/System.History", "value": a.text}]
    url = f"{tgt.org_url}/{tgt.project}/_apis/wit/workitems/{a.id}?api-version={API_VERSION}"
    http_json("PATCH", url, tgt.auth, patch, "application/json-patch+json")
    print("OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("ERROR:", ex)
        sys.exit(1)
