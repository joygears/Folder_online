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



const string_append = getTargetAddr(ptr(0x10054750));

send(string_append)


Interceptor.attach(string_append, {
    onEnter(args) {
        console.log("string_append onEnter")
       console.log("第一个参数:"+args[0].readUtf8String()," this对象: ",std_string_c_str(this.context.ecx))
    },
    onLeave(retval){
        console.log("string_append onLeave")
        console.log("返回值：" + std_string_c_str(retval))
    }
});





