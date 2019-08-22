"""
print(root.clipboard_get())
root.clipboard_append("fesfesf")
print(root.clipboard_get())
"""
import hashlib

import hashlib
m = hashlib.md5()
#m.update("000005fab4534d05api_key9a0554259914a86fb9e7eb014e4e5d52permswrite")
m.update("test data".encode("utf-8"))
print(m.hexdigest())

print(hashlib.sha256("Nobody inspects the spammish repetition".encode("utf-8")).hexdigest())


h = hashlib.new('sha256')
h.update("Nobody inspects the spammish repetition".encode("utf-8"))
print(h.hexdigest())