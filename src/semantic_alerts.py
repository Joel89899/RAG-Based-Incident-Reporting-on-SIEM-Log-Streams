"""Helper to build deterministic, ATT&CK-enriched natural-language alert sentences

This module provides `build_semantic_alert(row)` which converts a pandas.Series
representing a network/log record into a short, deterministic natural-language
sentence enriched with inferred service names and MITRE ATT&CK tactic hints.

Motivation/citations:
- Qwen3 (entry 9) injects tactic/protocol context into event sentences before
  embedding; the paper notes that ~26% of misclassifications were due to
  context-window limitations that grouping (community detection) helps address.
- ReGAIN (entry 14) uses deterministic NL summarization of structured 5-tuple
  records before embedding on CIC-family data — useful prior art for this design.

The function is intentionally deterministic (no randomness/LLM) so embeddings are
stable and comparable across runs.
"""
from typing import Optional

# Common port -> service mapping (extend as needed)
PORT_SERVICE = {
    22: "SSH",
    23: "Telnet",
    21: "FTP",
    20: "FTP-data",
    80: "HTTP",
    443: "HTTPS",
    53: "DNS",
    3389: "RDP",
    445: "SMB",
    139: "NetBIOS",
    3306: "MySQL",
    1433: "MSSQL",
    25: "SMTP",
    5900: "VNC",
    161: "SNMP",
    389: "LDAP",
    5060: "SIP",
}

# Simple service -> ATT&CK hint mapping
SERVICE_HINT = {
    "SSH": "possible credential access via SSH (Credential Access / Lateral Movement)",
    "RDP": "possible credential access or remote execution via RDP (Credential Access / Lateral Movement)",
    "SMB": "possible lateral movement or file access via SMB (Lateral Movement / Exfiltration)",
    "HTTP": "possible command-and-control or data transfer over HTTP (Command and Control / Exfiltration)",
    "HTTPS": "possible command-and-control or data transfer over HTTPS (Command and Control / Exfiltration)",
    "DNS": "possible tunnelling or data exfiltration via DNS (Command and Control / Exfiltration)",
    "FTP": "possible file transfer via FTP (Exfiltration)",
    "SMTP": "possible data exfiltration or phishing-related activity via SMTP (Exfiltration / Initial Access)",
    "Telnet": "possible credential access via Telnet (Credential Access)",
}


def _port_to_service(port: Optional[int]) -> Optional[str]:
    try:
        if port is None:
            return None
        port = int(port)
    except Exception:
        return None
    return PORT_SERVICE.get(port)


def build_semantic_alert(row) -> str:
    """Build a deterministic NL alert sentence enriched with service and ATT&CK hint.

    Expects `row` to be a mapping-like object (e.g., pandas.Series) with common
    fields: 'SrcIP'/'Source'/'src_ip', 'DstIP'/'Destination'/'dst_ip', 'SrcPort',
    'DstPort', 'Protocol', and optional 'Label'/'AlertType'. The function will
    gracefully handle missing fields.
    """
    # resolve fields with common fallback names
    def _get(k1, k2=None):
        for k in (k1, k2) if k2 else (k1,):
            if k in row and row[k] is not None:
                return row[k]
        return None

    src = _get('SrcIP', 'source') or _get('src_ip') or _get('src') or 'UNKNOWN_SRC'
    dst = _get('DstIP', 'destination') or _get('dst_ip') or _get('dst') or 'UNKNOWN_DST'
    sport = _get('SrcPort', 'sport')
    dport = _get('DstPort', 'dport') or _get('DstPort')
    proto = (_get('Protocol') or _get('protocol') or '').upper()
    label = _get('Label') or _get('label') or _get('AlertType') or ''

    # infer service and hint
    service = _port_to_service(dport) or _port_to_service(sport)
    hint = SERVICE_HINT.get(service, '')

    # Build deterministic sentence parts
    parts = []
    parts.append(f"{src} -> {dst}")
    if sport or dport:
        sport_s = str(sport) if sport is not None else ''
        dport_s = str(dport) if dport is not None else ''
        parts.append(f"ports={sport_s}->{dport_s}")
    if proto:
        parts.append(f"proto={proto}")
    if service:
        parts.append(f"service={service}")
    if label:
        parts.append(f"label={label}")

    # Add ATT&CK hint deterministically at end if available
    if hint:
        parts.append(f"hint={hint}")

    sentence = "; ".join(p for p in parts if p)
    # Keep sentences short to fit typical embedding context windows
    return sentence[:512]
