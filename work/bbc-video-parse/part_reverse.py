import code

from uncompyle6.main import decompile
import sys
# version = (3, 7, 0)
import dis

def get_sub_codeObject_list(co):
    return [ins for ins in list(dis.Bytecode(co)) if "code object" in str(ins.argval)]

outstream = sys.stdout
showasm = None
showast = False
showgrammar = False
source_encoding = None
mapstream = None
do_fragments = False

from xdis import load_module
filename = "./result/core.pyc"
code_objects = {}
(version, timestamp, magic_int, co, is_pypy, source_size, sip_hash) = load_module(
    filename, code_objects
)

def decompile_part(co,father_name=None,outstream=sys.stdout):
    try:
        if father_name is not None:
            name = "%s.%s" % (father_name,co.co_name)
        else:
            name = co.co_name
        outstream.write("\n# %s ____________________________________________\n" % name)
        decompile(
            version,
            co,
            outstream,
            None,
            False,
            timestamp,
            False,
            None,
            code_objects={},
            source_size=source_size,
            is_pypy=False,
            magic_int=magic_int,
            mapstream=None,
            do_fragments=False,
        )
    except Exception as e:
        bytecode = get_sub_codeObject_list(co)
        for code in bytecode:
            co = code.argval
            decompile_part(co,name,outstream)
decompile_part(co)





