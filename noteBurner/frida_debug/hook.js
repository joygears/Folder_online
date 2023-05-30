var ASLR_baseAddress = Module.findBaseAddress("widevinecdm.dll");
var baseAddress = ptr(0x10000000);

function getTargetAddr(VA){
    return VA.sub(baseAddress).add(ASLR_baseAddress);
}

function std_string_c_str(str){
     var  size = ptr(str).add(0x10).readU32();
        if(size < 0x0F)
           return  str.readUtf8String()
        else
          return ptr(str.readU32()).readUtf8String()

    }



const string_append = getTargetAddr(ptr(0x1005AD10));

send(string_append)


Interceptor.attach(string_append, {
    onEnter(args) {
        console.log("sub_1005AD10 onEnter")
        var pNode = ptr(ptr(this.context.ecx).readU32());

        console.log("root------------------------------------: ",pNode);
        console.log("左节点: ",ptr(pNode.readU32()));
        console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
        console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
        pNode = ptr(pNode.readU32());
        console.log("head ------------------------------------: ",pNode);
        console.log("左节点: ",ptr(pNode.readU32()));
        console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
        console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
        console.log("is Head: ",ptr(pNode.add(0xD).readU8()));

      // console.log("第一个参数:"+args[0].readUtf8String()," this对象: ",std_string_c_str(this.context.ecx))
    },
    onLeave(retval){
        console.log("sub_1005AD10 onLeave")
        //console.log("返回值：" + std_string_c_str(retval))
    }
});





