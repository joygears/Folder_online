
 function stringToByte(str) {
    var bytes = new Array();
    var len, c;
    len = str.length;
    for(var i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if(c >= 0x010000 && c <= 0x10FFFF) {
            bytes.push(((c >> 18) & 0x07) | 0xF0);
            bytes.push(((c >> 12) & 0x3F) | 0x80);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        } else if(c >= 0x000800 && c <= 0x00FFFF) {
            bytes.push(((c >> 12) & 0x0F) | 0xE0);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        } else if(c >= 0x000080 && c <= 0x0007FF) {
            bytes.push(((c >> 6) & 0x1F) | 0xC0);
            bytes.push((c & 0x3F) | 0x80);
        } else {
            bytes.push(c & 0xFF);
        }
    }
    return bytes;


}

(function() {
    for (var hb = {}, fb = {}, eb = {
        "=": 0,
        ".": 0
    }, bb = {
        "=": 0,
        ".": 0
    }, lb = /\s+/g, pb = /^[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/_-]*[=]{0,2}$/, kb = 64; kb--; ) {
        hb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")[kb]] = 262144 * kb;
        fb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")[kb]] = 4096 * kb;
        eb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")[kb]] = 64 * kb;
        bb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")[kb]] = kb;
    }
    for (kb = 64; kb-- && ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")[kb] != ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")[kb]; ) {
        hb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")[kb]] = 262144 * kb;
        fb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")[kb]] = 4096 * kb;
        eb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")[kb]] = 64 * kb;
        bb[("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")[kb]] = kb;
    }
    Cb = function(Ha, Ma) {
        for (var Qa = "", za = 0, na = Ha.length, ha = na - 2, ba = Ma ? "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", ca = Ma ? "" : "="; za < ha; ) {
            Ma = 65536 * Ha[za++] + 256 * Ha[za++] + Ha[za++];
            Qa += ba[Ma >>> 18] + ba[Ma >>> 12 & 63] + ba[Ma >>> 6 & 63] + ba[Ma & 63];
        }
        za == ha ? (Ma = 65536 * Ha[za++] + 256 * Ha[za++],
        Qa += ba[Ma >>> 18] + ba[Ma >>> 12 & 63] + ba[Ma >>> 6 & 63] + ca) : za == na - 1 && (Ma = 65536 * Ha[za++],
        Qa += ba[Ma >>> 18] + ba[Ma >>> 12 & 63] + ca + ca);
        return Qa;
    }
    ;
    Fb = function(Ha, Ma) {
        Ha = Ha.replace(lb, "");
        if (Ma && (Ma = Ha.length % 4)) {
            Ma = 4 - Ma;
            for (var Qa = 0; Qa < Ma; ++Qa) {
                Ha += "=";
            }
        }
        Ma = Ha.length;
        if (0 != Ma % 4 || !pb.test(Ha))
            throw Error("bad base64: " + Ha);
        for (var za = Ma / 4 * 3 - ("=" == Ha[Ma - 1] ? 1 : 0) - ("=" == Ha[Ma - 2] ? 1 : 0), na = new Uint8Array(za), ha = 0, ba = 0; ha < Ma; ) {
            Qa = hb[Ha[ha++]] + fb[Ha[ha++]] + eb[Ha[ha++]] + bb[Ha[ha++]];
            na[ba++] = Qa >>> 16;
            ba < za && (na[ba++] = Qa >>> 8 & 255,
            ba < za && (na[ba++] = Qa & 255));
        }
        return na;
    }
    ;
}
)();
 function byteToString(arr) {
    if(typeof arr === 'string') {
        return arr;
    }
    var str = '',
        _arr = arr;
    for(var i = 0; i < _arr.length; i++) {
        var one = _arr[i].toString(2),
            v = one.match(/^1+?(?=0)/);
        if(v && one.length == 8) {
            var bytesLength = v[0].length;
            var store = _arr[i].toString(2).slice(7 - bytesLength);
            for(var st = 1; st < bytesLength; st++) {
                store += _arr[st + i].toString(2).slice(2);
            }
            str += String.fromCharCode(parseInt(store, 2));
            i += bytesLength - 1;
        } else {
            str += String.fromCharCode(_arr[i]);
        }
    }
    return str;
}
(function() {
    var bb, lb, pb;
    function hb(kb, Ha) {
        Ha || (Ha = kb.length);
        return kb.reduce(function(Ma, Qa, za) {
            return za < Ha ? Ma + String.fromCharCode(Qa) : Ma;
        }, "");
    }
    for (var fb = {}, eb = 0; 256 > eb; ++eb) {
        bb = hb([eb]);
        fb[bb] = eb;
    }
    lb = Object.keys(fb).length;
    pb = [];
    for (eb = 0; 256 > eb; ++eb) {
        pb[eb] = [eb];
    }
    qe = function(kb, Ha) {
        var U, Y;
        function Ma(sa, pa) {
            var ta;
            for (; 0 < pa; ) {
                if (ca >= ba.length)
                    return !1;
                if (pa > ia) {
                    ta = sa;
                    ta >>>= pa - ia;
                    ba[ca] |= ta & 255;
                    pa -= ia;
                    ia = 8;
                    ++ca;
                } else
                    pa <= ia && (ta = sa,
                    ta <<= ia - pa,
                    ta &= 255,
                    ta >>>= 8 - ia,
                    ba[ca] |= ta & 255,
                    ia -= pa,
                    pa = 0,
                    0 == ia && (ia = 8,
                    ++ca));
            }
            return !0;
        }
        for (var Qa in fb) {
            Ha[Qa] = fb[Qa];
        }
        for (var za = lb, na = [], ha = 8, ba = new Uint8Array(kb.length), ca = 0, ia = 8, fa = 0; fa < kb.length; ++fa) {
            U = kb[fa];
            na.push(U);
            Qa = hb(na);
            Y = Ha[Qa];
            if (!Y) {
                na = hb(na, na.length - 1);
                if (!Ma(Ha[na], ha))
                    return null;
                0 != za >> ha && ++ha;
                Ha[Qa] = za++;
                na = [U];
            }
        }
        return 0 < na.length && (Qa = hb(na),
        Y = Ha[Qa],
        !Ma(Y, ha)) ? null : ba.subarray(0, 8 > ia ? ca + 1 : ca);
    }
    ;
    re = function(kb) {
        var fa, U;
        for (var Ha = pb.slice(), Ma = 0, Qa = 0, za = 8, na = new Uint8Array(Math.ceil(1.5 * kb.length)), ha = 0, ba, ca = []; Ma < kb.length && !(8 * (kb.length - Ma) - Qa < za); ) {
            for (var ia = ba = 0; ia < za; ) {
                fa = Math.min(za - ia, 8 - Qa);
                U = kb[Ma];
                U <<= Qa;
                U &= 255;
                U >>>= 8 - fa;
                ia += fa;
                Qa += fa;
                8 == Qa && (Qa = 0,
                ++Ma);
                ba |= (U & 255) << za - ia;
            }
            ia = Ha[ba];
            0 == ca.length ? ++za : (ia ? ca.push(ia[0]) : ca.push(ca[0]),
            Ha[Ha.length] = ca,
            ca = [],
            Ha.length == 1 << za && ++za,
            ia || (ia = Ha[ba]));
            ba = ha + ia.length;
            ba >= na.length && (fa = new Uint8Array(Math.ceil(1.5 * ba)),
            fa.set(na),
            na = fa);
            na.set(ia, ha);
            ha = ba;
            ca = ca.concat(ia);
        }
        return na.subarray(0, ha);
    }
    ;
}
)();
// lzw_encode=qe
// lzw_decode=re
// string = '{"version":2,"url":"licensedManifest","id":165329016374135650,"languages":["en-TW"],"params":{"type":"standard","manifestVersion":"v2","viewableId":81509456,"profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"],"flavor":"STANDARD","drmType":"widevine","drmVersion":25,"usePsshBox":true,"isBranching":false,"useHttpsStreams":true,"supportsUnequalizedDownloadables":true,"imageSubtitleHeight":1080,"uiVersion":"shakti-v4f4fb02e","uiPlatform":"SHAKTI","clientVersion":"6.0035.000.911","supportsPreReleasePin":true,"supportsWatermark":true,"videoOutputInfo":[{"type":"DigitalVideoOutputDescriptor","outputType":"unknown","supportedHdcpVersions":[],"isHdcpEngaged":false}],"titleSpecificData":{"81509456":{"unletterboxed":false}},"preferAssistiveAudio":false,"isUIAutoPlay":false,"isNonMember":false,"desiredVmaf":"plus_lts","desiredSegmentVmaf":"plus_lts","requestSegmentVmaf":false,"supportsPartialHydration":false,"contentPlaygraph":["start"],"challenges":{"default":[{"drmSessionId":"9DC6975C72BA7FB0FBC979E67EDF8F29","clientTime":1653290163,"challengeBase64":"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"}]},"profileGroups":[{"name":"default","profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"]}],"licenseType":"standard","xid":"165329016333614430","showAllSubDubTracks":false}}'
// buffer = stringToByte(string)
// sa = {}
// lzw_buffer = lzw_encode(buffer,sa)
// buffer = lzw_decode(lzw_buffer)
// string =byteToString(buffer)
// console.log(string)
function lzw_encode(string){
    buffer = stringToByte(string)
    sa = {}
    lzw_buffer = qe(buffer,sa)
    return lzw_buffer;
}
function lzw_decode(source){
    buffer = Fb(source)
    plaintext_buffer = re(buffer);
    plaintext = new TextDecoder().decode(plaintext_buffer);
    return plaintext;
}


