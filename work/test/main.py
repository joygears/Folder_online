import dis
from xdis import load_module


def get_sub_codeObject_list(co):
    return [ins for ins in list(dis.Bytecode(co)) if "code object" in str(ins.argval)]


code_objects = {}
filename = "./core.pyc"


(version, timestamp, magic_int, co, is_pypy, source_size, sip_hash) = load_module(
    filename, code_objects
)

bytecode = get_sub_codeObject_list(co)
co =  bytecode[0].argval

co = list(dis.Bytecode(co))
co.append(dis.Instruction("RETURN_LAST", None,
                   None, None, None,
                   -1, None, None))
print(co)