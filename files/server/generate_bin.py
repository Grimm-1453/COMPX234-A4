import os
with open('testfile.bin', 'wb') as f:
    f.write(os.urandom(50 * 1024))  # 50KB
with open('bigfile.dat', 'wb') as f:
    f.write(os.urandom(5 * 1024 * 1024))  # 5MB