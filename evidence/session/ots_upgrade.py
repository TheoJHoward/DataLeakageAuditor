"""Pure-Python OpenTimestamps receipt upgrade (no python-bitcoinlib, no ctypes).

Queries each calendar named in a PendingAttestation for the completed timestamp
tree, merges it, and writes the upgraded receipt to OUT. Also cross-checks the
Bitcoin attestation's merkle root against blockstream.info's block index.
Read-only on the input; writes only to OUT.
"""
import hashlib
import json
import sys
import urllib.request

from opentimestamps.core.notary import BitcoinBlockHeaderAttestation, PendingAttestation
from opentimestamps.core.serialize import (
    BytesDeserializationContext,
    StreamDeserializationContext,
    StreamSerializationContext,
)
from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp

IN_OTS, IN_FILE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

with open(IN_OTS, "rb") as f:
    detached = DetachedTimestampFile.deserialize(StreamDeserializationContext(f))

with open(IN_FILE, "rb") as f:
    actual_digest = hashlib.sha256(f.read()).digest()
print(f"digest match vs {IN_FILE}: {detached.file_digest == actual_digest}")

def walk(ts):
    yield ts
    for stamp in ts.ops.values():
        yield from walk(stamp)

pending_before = [a for _, a in detached.timestamp.all_attestations() if isinstance(a, PendingAttestation)]
btc_before = [a for _, a in detached.timestamp.all_attestations() if isinstance(a, BitcoinBlockHeaderAttestation)]
print(f"before: {len(pending_before)} pending, {len(btc_before)} bitcoin")

for node in walk(detached.timestamp):
    for att in list(node.attestations):
        if not isinstance(att, PendingAttestation):
            continue
        url = att.uri.rstrip("/") + "/timestamp/" + node.msg.hex()
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/vnd.opentimestamps.v1", "User-Agent": "python-opentimestamps"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            node.merge(Timestamp.deserialize(BytesDeserializationContext(data), node.msg))
            print(f"upgraded from {att.uri}")
        except Exception as e:
            print(f"calendar {att.uri}: {type(e).__name__}: {e}")

btc_after = [(msg, a) for msg, a in detached.timestamp.all_attestations() if isinstance(a, BitcoinBlockHeaderAttestation)]
print(f"after: {len(btc_after)} bitcoin attestation(s)")
if not btc_after:
    print("NOT YET ELIGIBLE — no calendar returned a Bitcoin attestation; try again later")
    sys.exit(2)

for msg, att in btc_after:
    print(f"bitcoin block height: {att.height}")
    try:
        with urllib.request.urlopen(f"https://blockstream.info/api/block-height/{att.height}", timeout=30) as r:
            block_hash = r.read().decode().strip()
        with urllib.request.urlopen(f"https://blockstream.info/api/block/{block_hash}", timeout=30) as r:
            block = json.loads(r.read())
        ok = msg[::-1].hex() == block["merkle_root"]
        print(f"  block {block_hash} timestamp {block['timestamp']} merkle_root match: {ok}")
        if not ok:
            print(f"  EXPECTED {block['merkle_root']}  GOT {msg[::-1].hex()}")
            sys.exit(3)
    except Exception as e:
        print(f"  merkle cross-check unavailable ({type(e).__name__}: {e}) — attestation still merged")

with open(OUT, "wb") as f:
    detached.serialize(StreamSerializationContext(f))

with open(OUT, "rb") as f:
    reparsed = DetachedTimestampFile.deserialize(StreamDeserializationContext(f))
roundtrip_btc = [a for _, a in reparsed.timestamp.all_attestations() if isinstance(a, BitcoinBlockHeaderAttestation)]
print(f"roundtrip: digest match {reparsed.file_digest == actual_digest}, bitcoin attestations {len(roundtrip_btc)}")
print("UPGRADE COMPLETE")
