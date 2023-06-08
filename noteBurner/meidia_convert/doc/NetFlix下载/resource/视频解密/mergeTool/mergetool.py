import sys
import os
if(len(sys.argv) != 1):
    filenames = sys.argv[1:]
    total_bytes = []
    target = bytes()
    for filename in filenames:
        with open(filename,"rb") as fp:
            total_bytes.append(fp.read())
    for t in total_bytes:
        target += t
    dir,_ = os.path.split(filenames[0])
    out_filename = os.path.join(dir,"temp.bin")
    with open(out_filename,"wb") as fp:
        fp.write(target)
    print("merge Successfull out to "+out_filename)
else:
    print("incorect format plase input like this mergetool file1 file2 ...")

