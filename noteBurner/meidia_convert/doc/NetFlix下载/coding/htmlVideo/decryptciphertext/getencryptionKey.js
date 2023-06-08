//1.通过定位unwrapKey(,将unwrapKey(的第6个参数改为1，并删除indexDB数据库

//2.再将下面的代码插入片段，在入口如断下，执行片段即可获取encryptionkey的base64
function _arrayBufferToBase64( buffer ) {
    var binary = '';
    var bytes = new Uint8Array( buffer );
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode( bytes[ i ] );
    }
    return window.btoa( binary );
  }
  async function exportCryptoKey(key) {
  let exported = await window.crypto.subtle.exportKey(
    "raw",
    key
  );
  
  return _arrayBufferToBase64(exported);
  }
  async function middleline(result){
    let encryptionkey =await exportCryptoKey(result.data.encryptionKey);
    let hmacKey = await exportCryptoKey(result.data.hmacKey);
    console.log("encryptionKey: "+encryptionkey);
    console.log("hmacKey: "+hmacKey);

  }
  let request = window.indexedDB.open("netflix.player");
  request.onsuccess = function() {
  let db = request.result;
  let namedata = db.transaction("namedatapairs","readwrite");
  let mslstore = namedata .objectStore("namedatapairs")["get"]("mslstore");
  mslstore.onsuccess = function(event) {
                                    result = event.target.result;
                                    middleline(this.result);
                        }
  // 继续使用 db 对象处理数据库
  };
  