#!/usr/bin/env python3
"""DELTA R67 / §17.3 - resolve §3.5's circular README instruction.

VERIFIED FIRST, as §17.3 requires: C2's expression is `git show ":$f" | sha256sum`,
and `git show :<path>` reads the INDEX. Proven in a throwaway repo against three
distinguishable states (HEAD-VERSION / INDEX-VERSION / WORKTREE-VERSION): the
expression returned INDEX-VERSION. So C2 hashes STAGED content, the condition
§17.3 makes the fix conditional on holds, and the circularity is a WORDING defect,
not a live ceremony defect.
"""
import pathlib

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "evidence/ceremony/CEREMONY_COMMANDS.md")
s = P.read_text(encoding="utf-8")
EM = "\u2014"; S = "\u00a7"

OLD = ("`README.md`'s new v30a block is filled from `v30a.hashes.txt` the same way, and is staged and\n"
       "committed **before** C2 runs " + EM + " so it is part of the commit the tag points at. `README.md` is not\n"
       "one of the six and is not self-referentially hashed.\n")

NEW = ("### 3.5.1 `README.md`'s v30a block " + EM + " the ordering, stated so it is not circular\n"
       "\n"
       "*(Until R67/" + S + "17.3 this read \"filled from `v30a.hashes.txt` " + EM + " and is staged and committed\n"
       "**before** C2 runs\". `v30a.hashes.txt` is C2's **output** (" + S + "3.4: \"the only place any `prereg-v30a`\n"
       "hash value is produced\"), so as written the block had to be filled from a file that did not\n"
       "yet exist. Corrected to the executable order below.)*\n"
       "\n"
       "**The order, and it is not circular because `README.md` is NOT one of the six:**\n"
       "\n"
       "1. `git add` the six and everything else in `COMMIT_PLAN.md` " + S + "4 **except `README.md`**.\n"
       "2. **C2** " + EM + " hashes **staged** content (`git show :<path>`, " + S + "3.4) " + EM + "> `v30a.hashes.txt`.\n"
       "3. Fill `README.md`'s v30a block from `v30a.hashes.txt`. Never retyped.\n"
       "4. `git add README.md`.\n"
       "5. `git commit` " + EM + " so `README.md` IS in the commit the tag points at, which is what the old\n"
       "   wording was reaching for.\n"
       "6. Write `tagmsg.txt` from the same `v30a.hashes.txt`, then tag.\n"
       "\n"
       "**Why step 4 cannot move a single one of the six.** The six hashes were read at step 2 from the\n"
       "index entries for `$FILES`. `README.md` is not in `$FILES`, so staging it adds an index entry\n"
       "that no hash in the block covers. **C2g** (" + S + "3.6) re-reads the six out of the finished commit and\n"
       "must still match `v30a.hashes.txt`; that is the gate which would catch it if this reasoning were\n"
       "wrong, and it is not waived here.\n"
       "\n"
       "**`README.md` is not one of the six and is not self-referentially hashed** " + EM + " it carries the block,\n"
       "so hashing it would require its own hash to be inside itself. `PREREG.md` " + S + "11 item 3 puts the block\n"
       "\"in the tag message **and the README**\": two loci, one source, and that source is `v30a.hashes.txt`.\n")

n = s.count(OLD)
assert n == 1, "match count %d, expected 1" % n
P.write_text(s.replace(OLD, NEW, 1), encoding="utf-8")
print("CEREMONY_COMMANDS.md \u00a73.5 : circular README instruction replaced by \u00a73.5.1's six-step order")
print("  verified precondition   : C2 reads the INDEX (git show :<path>), proven empirically")
