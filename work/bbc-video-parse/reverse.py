# from  uncompyle6.bin.uncompile import main_bin
# main_bin()
import dis
import marshal
import sys
# filename = "./__pycache__/bilibili.cpython-37.pyc"
# filename = "./__pycache__/bbc.cpython-37.pyc"
if len(sys.argv) == 2:
    filename = sys.argv[1]
    #filename = "./__pycache__/Test.cpython-37.pyc"

    with open(filename,"rb") as fp:
        byteCode = fp.read()[16:]
    def Hello():
        print("hello world")

    co  = marshal.loads(byteCode)
    dis.dis(co)
    # bytecode = list(dis.Bytecode(co))




