"""
MCP Server for Acoustic Stapedial Reflex Threshold (ART) Skill.
Exposes JSON-RPC Model Context Protocol tools for evaluating acoustic reflex thresholds, sensation levels, and reflex decay rates.
"""

import sys
import json
from typing import Dict, Any
from client import AcousticStapedialReflexClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_stapedial_reflex",
                "description": "Calculates Acoustic Stapedial Reflex Thresholds (ART in dB HL), Sensation Level (SL in dB), 10-second reflex decay, and middle-ear protective resilience score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ipsilateral_threshold_db_hl": {
                            "type": "number",
                            "description": "Ipsilateral acoustic reflex threshold in dB HL (e.g. 80.0 dB HL, normative 70-95 dB HL)."
                        },
                        "contralateral_threshold_db_hl": {
                            "type": "number",
                            "description": "Contralateral acoustic reflex threshold in dB HL (e.g. 85.0 dB HL)."
                        },
                        "stimulus_freq_hz": {
                            "type": "integer",
                            "description": "Pure-tone stimulus frequency in Hz (500, 1000, 2000, or 4000 Hz, default: 1000).",
                            "default": 1000
                        },
                        "reflex_decay_10s_pct": {
                            "type": "number",
                            "description": "Reflex amplitude decay percentage after 10 s at +10 dB SL (normative < 50%, default: 15.0%).",
                            "default": 15.0
                        },
                        "hearing_threshold_db_hl": {
                            "type": "number",
                            "description": "Pure tone audiometric baseline hearing threshold in dB HL (default: 15.0 dB HL).",
                            "default": 15.0
                        }
                    },
                    "required": ["ipsilateral_threshold_db_hl", "contralateral_threshold_db_hl"]
                }
            }
        ]
    }


def handle_request(client: AcousticStapedialReflexClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_stapedial_reflex":
            decay = args.get("reflex_decay_10s_pct")
            res = client.evaluate_stapedial_reflex(
                ipsilateral_threshold_db_hl=float(args.get("ipsilateral_threshold_db_hl", 80.0)),
                contralateral_threshold_db_hl=float(args.get("contralateral_threshold_db_hl", 85.0)),
                stimulus_freq_hz=int(args.get("stimulus_freq_hz", 1000)),
                reflex_decay_10s_pct=float(decay) if decay is not None else 15.0,
                hearing_threshold_db_hl=float(args.get("hearing_threshold_db_hl", 15.0))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {name}"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": f"Invalid Request: Unsupported method {method}"
            }
        }


def main():
    client = AcousticStapedialReflexClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error or exception: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
