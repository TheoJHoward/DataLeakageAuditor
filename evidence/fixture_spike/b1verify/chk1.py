import hashlib
D = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md"
N = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\7c596505-0a64-4426-b893-56cc712b606c\scratchpad_lost_edit_new.txt"
d = open(D,'rb').read()
n = open(N,'rb').read()
print("decl bytes", len(d), "sha256", hashlib.sha256(d).hexdigest())
print("decl newline counts: CRLF", d.count(b'\r\n'), "LF", d.count(b'\n'), "CR", d.count(b'\r'))
print("new bytes", len(n), "sha256", hashlib.sha256(n).hexdigest())
print("new newline counts: CRLF", n.count(b'\r\n'), "LF", n.count(b'\n'), "CR", n.count(b'\r'))
print("raw containment count:", d.count(n))
i = d.find(n)
print("raw find idx:", i)
# normalized comparison
dn = d.replace(b'\r\n', b'\n')
nn = n.replace(b'\r\n', b'\n')
print("normalized containment count:", dn.count(nn), "idx", dn.find(nn))
# heading occurrences
h = b"#### A.6.0"
print("heading occurrences:", d.count(h))
