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

console.log(_arrayBufferToBase64(exported));
}

let request = window.indexedDB.open("netflix.player");
request.onsuccess = function() {
let db = request.result;
let namedata = db.transaction("namedatapairs","readwrite");
let mslstore = namedata .objectStore("namedatapairs")["get"]("mslstore");
mslstore.onsuccess = function(event) {
                                  result = event.target.result;
                                  exportCryptoKey(result.data.encryptionKey);
                      }
// 继续使用 db 对象处理数据库
};
