import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rpc.rpc_server import rpc_server

rpc_server().online()
    