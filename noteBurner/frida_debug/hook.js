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



// const json__toStyledString = getTargetAddr(ptr(0x10052060));

// send(json__toStyledString)


// Interceptor.attach(json__toStyledString, {
//     onEnter(args) {
//         console.log("json__toStyledString onEnter")
//         // pNode = ptr(ptr(this.context.ecx).readU32());

//         // console.log("root------------------------------------: ",pNode);
//         // console.log("左节点: ",ptr(pNode.readU32()));
//         // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
//         // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
//         // pNode = ptr(pNode.readU32());
//         // console.log("head ------------------------------------: ",pNode);
//         // console.log("左节点: ",ptr(pNode.readU32()));
//         // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
//         // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
//         // console.log("is Head: ",ptr(pNode.add(0xD).readU8()));
//         // pNode = ptr(ptr(this.context.ecx).readU32());
//       // console.log("第一个参数:"+args[0].readUtf8String()," this对象: ",std_string_c_str(this.context.ecx))
//       //console.log("第一个参数:"+std_string_c_str(args[1]))
//       //console.log("第二个参数:"+std_string_c_str(args[2]))
//     },
//     onLeave(retval){
//         console.log("json__toStyledString onLeave")
//         // console.log("root------------------------------------: ",pNode);
//         // console.log("左节点: ",ptr(pNode.readU32()));
//         // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
//         // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
//         console.log("send：" + std_string_c_str(retval))
//     }
// });


// const getJosnFromString = getTargetAddr(ptr(0x1006FC90));

// send(getJosnFromString)


// Interceptor.attach(getJosnFromString, {
//     onEnter(args) {
//         console.log("getJosnFromString onEnter")
//         // pNode = ptr(ptr(this.context.ecx).readU32());

//         // console.log("root------------------------------------: ",pNode);
//         // console.log("左节点: ",ptr(pNode.readU32()));
//         // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
//         // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
//         // pNode = ptr(pNode.readU32());
//         // console.log("head ------------------------------------: ",pNode);
//         // console.log("左节点: ",ptr(pNode.readU32()));
//         // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
//         // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
//         // console.log("is Head: ",ptr(pNode.add(0xD).readU8()));
//         // pNode = ptr(ptr(this.context.ecx).readU32());
//       // console.log("第一个参数:"+args[0].readUtf8String()," this对象: ",std_string_c_str(this.context.ecx))
//       console.log("recv: "+std_string_c_str(args[1]))
//       //console.log("第二个参数:"+std_string_c_str(args[2]))
//     },
//     onLeave(retval){
//         console.log("getJosnFromString onLeave")
//         // console.log("root------------------------------------: ",pNode);
//         // console.log("左节点: ",ptr(pNode.readU32()));
//         // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
//         // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
//         //console.log("返回值：" + std_string_c_str(retval))
//     }
// });


const InitializeVideoDecoder = getTargetAddr(ptr(0x102125B0));

send(InitializeVideoDecoder)


Interceptor.attach(InitializeVideoDecoder, {
    onEnter(args) {
        console.log("InitializeVideoDecoder onEnter")
        // pNode = ptr(ptr(this.context.ecx).readU32());

        // console.log("root------------------------------------: ",pNode);
        // console.log("左节点: ",ptr(pNode.readU32()));
        // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
        // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
        // pNode = ptr(pNode.readU32());
        // console.log("head ------------------------------------: ",pNode);
        // console.log("左节点: ",ptr(pNode.readU32()));
        // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
        // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
        // console.log("is Head: ",ptr(pNode.add(0xD).readU8()));
        // pNode = ptr(ptr(this.context.ecx).readU32());
      // console.log("第一个参数:"+args[0].readUtf8String()," this对象: ",std_string_c_str(this.context.ecx))
      console.log("第一个参数: "+ hexdump(ptr(args[0])));
     // console.log("第二个参数: "+ args[1].readUtf8String())
    },
    onLeave(retval){
        console.log("InitializeVideoDecoder onLeave")
        // console.log("root------------------------------------: ",pNode);
        // console.log("左节点: ",ptr(pNode.readU32()));
        // console.log("父节点: ",ptr(pNode.add(0x4).readU32()));
        // console.log("左节点: ",ptr(pNode.add(0x8).readU32()));
        console.log("返回值：" + retval)
    }
});


// const DecryptAndDecodeFrame = getTargetAddr(ptr(0x10211E90));

// send(DecryptAndDecodeFrame)


// Interceptor.attach(DecryptAndDecodeFrame, {
    // onEnter(args) {
        // console.log("DecryptAndDecodeFrame onEnter")
     
      // console.log("第一个参数: "+ hexdump(ptr(args[0])));
    
    // },
    // onLeave(retval){
        // console.log("DecryptAndDecodeFrame onLeave")
    // }
// });

// // const DeinitializeDecoder = getTargetAddr(ptr(0x10212070));

// // send(DeinitializeDecoder)


// // Interceptor.attach(DeinitializeDecoder, {
    // // onEnter(args) {
        // // console.log("DeinitializeDecoder onEnter")
       
    // // },
    // // onLeave(retval){
        // // console.log("DeinitializeDecoder onLeave")
        
    // // }
// // });

// const ResetDecoder = getTargetAddr(ptr(0x10212B50));

// send(ResetDecoder)


// Interceptor.attach(ResetDecoder, {
    // onEnter(args) {
        // console.log("ResetDecoder onEnter")
		// console.log("decoder_type: ",ptr(args[0]).toInt32())
    // },
    // onLeave(retval){
        // console.log("ResetDecoder onLeave")
        
    // }
// });


//---------------------------------------- CreateProcess -----------------------------------------------
// var CreateProcess = Module.findExportByName("kernel32.dll","CreateProcessW");


// Interceptor.attach(CreateProcess, {
//     onEnter(args) {
//         console.log("CreateProcessW onEnter")

//       console.log("程序名: ",args[0].toInt32() != 0 ? args[0].readUtf16String():"省略","lpCommandLine: ",args[1].toInt32() != 0 ? args[1].readUtf16String():"无");
//     },
//     onLeave(retval){
//         console.log("CreateProcessW onLeave")
//         //console.log("返回值：" + std_string_c_str(retval))
//     }
// });

//----------------------------------------ws2_32.dll send() -----------------------------------------------
// var CreateProcess = Module.findExportByName("ws2_32.dll","WSASend");


// Interceptor.attach(CreateProcess, {
//     onEnter(args) {
//         console.log("WSASend onEnter")
//     var dwBufferCount = args[2].toInt32();
//     var lpBuffer = args[1];
//     console.log("dwBufferCount: ",dwBufferCount);

//     for(var i = 0;i<dwBufferCount;i++){
//         var len = lpBuffer.readU32();
//         console.log("send to  Server: ",ptr(lpBuffer.add(0x4).readU32()).readByteArray(len));
//         lpBuffer=lpBuffer.add(8);
//     }

//     },
//     onLeave(retval){
//         console.log("WSASend onLeave")
//         //console.log("返回值：" + std_string_c_str(retval))
//     }
// });



