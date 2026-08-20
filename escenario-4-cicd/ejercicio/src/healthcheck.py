import os
import sys
import urllib.request

port = os.environ.get("PORT", "3000")

try:
    with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=2) as res:
        sys.exit(0 if res.status == 200 else 1)
except Exception:
    sys.exit(1)
