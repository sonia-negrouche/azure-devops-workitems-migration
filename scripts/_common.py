#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared helpers for Azure DevOps REST (stdlib-only).

Public repo note:
- No hardcoded orgs/projects/PATs in this repo.
- Provide everything via env vars and/or CLI args.

Env vars (recommended):
  ADO_SOURCE_ORG_URL, ADO_SOURCE_PROJECT, ADO_SOURCE_PAT
  ADO_TARGET_ORG_URL, ADO_TARGET_PROJECT, ADO_TARGET_PAT
"""

from __future__ import annotations

import base64
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib import error, request


API_VERSION = "7.0"
COMMENTS_API_VERSION = "7.1-preview.3"


def env(name: str) -> str:
    return (os.getenv(name) or "").strip()


def require(value: str, what: str, env_name: Optional[str] = None) -> str:
    v = (value or "").strip()
    if not v:
        hint = f" (env {env_name})" if env_name else ""
        raise SystemExit(f"Missing required '{what}'{hint}. Provide CLI arg or set env var.")
    return v


def auth_header(pat: str) -> str:
    return "Basic " + base64.b64encode(f":{pat}".encode("ascii")).decode("ascii")


@dataclass(frozen=True)
class AdoConn:
    org_url: str
    project: str
    pat: str

    @property
    def auth(self) -> str:
        return auth_header(self.pat)


def http_json(method: str, url: str, auth: str, body: Any = None,
             content_type: str = "application/json", max_retries: int = 5) -> Any:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    for attempt in range(max_retries):
        req = request.Request(url, data=data, method=method)
        req.add_header("Authorization", auth)
        if body is not None:
            req.add_header("Content-Type", content_type)
        try:
            with request.urlopen(req) as resp:
                raw = resp.read()
                return json.loads(raw.decode("utf-8")) if raw else {}
        except error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(min(2 ** (attempt + 1), 60))
                continue
            raise RuntimeError(f"{method} {url} failed [{e.code}]: {msg[:1200]}")
        except error.URLError as e:
            if attempt < max_retries - 1:
                time.sleep(min(2 ** (attempt + 1), 60))
                continue
            raise RuntimeError(f"{method} {url} failed: {e}")


def http_binary(method: str, url: str, auth: str, body: Optional[bytes] = None,
                content_type: Optional[str] = None, max_retries: int = 5) -> bytes:
    for attempt in range(max_retries):
        req = request.Request(url, data=body, method=method)
        req.add_header("Authorization", auth)
        if content_type:
            req.add_header("Content-Type", content_type)
        try:
            with request.urlopen(req) as resp:
                return resp.read()
        except error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(min(2 ** (attempt + 1), 60))
                continue
            raise RuntimeError(f"{method} {url} failed [{e.code}]: {msg[:1200]}")
        except error.URLError as e:
            if attempt < max_retries - 1:
                time.sleep(min(2 ** (attempt + 1), 60))
                continue
            raise RuntimeError(f"{method} {url} failed: {e}")
