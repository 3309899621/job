window = global;
CryptoJS = require('crypto-js')
JSEncrypt = require("jsencrypt")
getRandomValues = require('get-random-values')

function getAesKeyAndRsaEncryptData() {
    var aesKey = function (t) {
        for (var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", r = "", n = 0; n < t; n++) {
            var i = Math.floor(Math.random() * e.length);
            r += e.substring(i, i + 1)
        }
        return r
    }(32);

    var e = new JSEncrypt();
    e.setPublicKey("-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnbJqzIXk6qGotX5nD521Vk/24APi2qx6C+2allfix8iAfUGqx0MK3GufsQcAt/o7NO8W+qw4HPE+RBR6m7+3JVlKAF5LwYkiUJN1dh4sTj03XQ0jsnd3BYVqL/gi8iC4YXJ3aU5VUsB6skROancZJAeq95p7ehXXAJfCbLwcK+yFFeRKLvhrjZOMDvh1TsMB4exfg+h2kNUI94zu8MK3UA7v1ANjfgopaE+cpvoulg446oKOkmigmc35lv8hh34upbMmehUqB51kqk9J7p8VMI3jTDBcMC21xq5XF7oM8gmqjNsYxrT9EVK7cezYPq7trqLX1fyWgtBtJZG7WMftKwIDAQAB-----END PUBLIC KEY-----");
    var rsaEncryptData = e.encrypt(aesKey);

    return {
        "aesKey": aesKey,
        "rsaEncryptData": rsaEncryptData
    }
}

function getXSHeader(aesKey, originalData, u){
    return jt(aesKey, originalData, u)
}

function getRequestData(aesKey, originalData){
    return Rt(JSON.stringify(originalData), aesKey)
}

function getResponseData(encryptData, aesKey){
    return It(encryptData, aesKey)
}

function getTraceparent(){
    return "00-" + E() + "-" + E(16) + "-" + "01"
}

function getXHttpToken(cookie){
    var document = {
        "cookie": cookie,
    }
    var _0x1f67 = ['documentElement', 'body', 'scrollLeft', 'clientLeft', 'clientY', 'scrollTop', 'clientTop', 'pageX', 'pageY', 'floor', 'random', 'trackImage_', 'onload', 'onerror', 'src', 'XMLHttpRequest', 'Microsoft', 'open', 'GET', '/wafcheck.json', 'send', 'getResponseHeader', 'replace', 'parse', 'substring', 'utrack', 'location', 'protocol', 'hostname', 'getTime', 'push', 'https://', 'host', '/utrack/track.gif', 'user_trace_token', 'X_HTTP_TOKEN', 'length', 'fromCharCode', 'concat', 'charAt', 'HTTP_JS_KEY', '(^|\x20)', '=([^;]*)(;|$)', 'cookie', 'match', '=;\x20expires=Thu,\x2001\x20Jan\x201970\x2000:00:00\x20UTC;\x20path=/;', 'event', 'tagName', 'BUTTON', 'INPUT', 'hidden-form-send', 'className', 'indexOf', 'target', 'srcElement', 'parentNode', 'log', 'clientX', 'ownerDocument'];
    (function(_0x4bd822, _0x2bd6f7) {
        var _0xb4bdb3 = function(_0x1d68f6) {
            while (--_0x1d68f6) {
                _0x4bd822['push'](_0x4bd822['shift']());
            }
        };
        _0xb4bdb3(++_0x2bd6f7);
    }(_0x1f67, 0x14b))
    var _0x3551 = function(_0x1e41ca, _0x165168) {
        _0x1e41ca = _0x1e41ca - 0x0;
        var _0x122898 = _0x1f67[_0x1e41ca];
        return _0x122898;
    };
    function _0xf848b6(_0x4fbd64, _0x42cba3) {
        var _0x19e6d = (_0x4fbd64 & 0xffff) + (_0x42cba3 & 0xffff);
        var _0x1729b3 = (_0x4fbd64 >> 0x10) + (_0x42cba3 >> 0x10) + (_0x19e6d >> 0x10);
        return _0x1729b3 << 0x10 | _0x19e6d & 0xffff;
    }
    function _0x670f4d(_0x4dc328, _0x25a720) {
        return _0x4dc328 << _0x25a720 | _0x4dc328 >>> 0x20 - _0x25a720;
    }
    function _0x2739f7(_0x1dea7d, _0x130596, _0x14480f, _0x596e8d, _0x2c995c, _0x22a611) {
        return _0xf848b6(_0x670f4d(_0xf848b6(_0xf848b6(_0x130596, _0x1dea7d), _0xf848b6(_0x596e8d, _0x22a611)), _0x2c995c), _0x14480f);
    }
    function _0xaa05ae(_0x2c21c6, _0x45bd1c, _0xc01eb5, _0x3ac73d, _0xecc463, _0x45185e, _0x36b67f) {
        return _0x2739f7(_0x45bd1c & _0xc01eb5 | ~_0x45bd1c & _0x3ac73d, _0x2c21c6, _0x45bd1c, _0xecc463, _0x45185e, _0x36b67f);
    }
    function _0x5a5634(_0x458dc9, _0x5a0340, _0xc0ee78, _0x2d51a1, _0x2c66d6, _0x7ade00, _0x53f7cf) {
        return _0x2739f7(_0x5a0340 & _0x2d51a1 | _0xc0ee78 & ~_0x2d51a1, _0x458dc9, _0x5a0340, _0x2c66d6, _0x7ade00, _0x53f7cf);
    }
    function _0x5d8807(_0x458674, _0x27821e, _0x26d3ea, _0x54241a, _0x2022a3, _0x62b675, _0x2b7662) {
        return _0x2739f7(_0x27821e ^ _0x26d3ea ^ _0x54241a, _0x458674, _0x27821e, _0x2022a3, _0x62b675, _0x2b7662);
    }
    function _0x318283(_0x3ff4d5, _0x48a086, _0x2a0228, _0x3f383b, _0x138e36, _0x35b7c8, _0x5bd9b4) {
        return _0x2739f7(_0x2a0228 ^ (_0x48a086 | ~_0x3f383b), _0x3ff4d5, _0x48a086, _0x138e36, _0x35b7c8, _0x5bd9b4);
    }
    function _0x45e748(_0x514574, _0x5ddbd2) {
        _0x514574[_0x5ddbd2 >> 0x5] |= 0x80 << _0x5ddbd2 % 0x20;
        _0x514574[(_0x5ddbd2 + 0x40 >>> 0x9 << 0x4) + 0xe] = _0x5ddbd2;
        var _0x406127;
        var _0x103546;
        var _0x896dff;
        var _0x5d8d82;
        var _0x5b6717;
        var _0x3894d9 = 0x67452301;
        var _0x8d34ed = -0x10325477;
        var _0x545346 = -0x67452302;
        var _0x17bf86 = 0x10325476;
        for (_0x406127 = 0x0; _0x406127 < _0x514574[_0x3551('0x0')]; _0x406127 += 0x10) {
            _0x103546 = _0x3894d9;
            _0x896dff = _0x8d34ed;
            _0x5d8d82 = _0x545346;
            _0x5b6717 = _0x17bf86;
            _0x3894d9 = _0xaa05ae(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127], 0x7, -0x28955b88);
            _0x17bf86 = _0xaa05ae(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x1], 0xc, -0x173848aa);
            _0x545346 = _0xaa05ae(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x2], 0x11, 0x242070db);
            _0x8d34ed = _0xaa05ae(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x3], 0x16, -0x3e423112);
            _0x3894d9 = _0xaa05ae(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x4], 0x7, -0xa83f051);
            _0x17bf86 = _0xaa05ae(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x5], 0xc, 0x4787c62a);
            _0x545346 = _0xaa05ae(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x6], 0x11, -0x57cfb9ed);
            _0x8d34ed = _0xaa05ae(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x7], 0x16, -0x2b96aff);
            _0x3894d9 = _0xaa05ae(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x8], 0x7, 0x698098d8);
            _0x17bf86 = _0xaa05ae(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x9], 0xc, -0x74bb0851);
            _0x545346 = _0xaa05ae(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xa], 0x11, -0xa44f);
            _0x8d34ed = _0xaa05ae(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0xb], 0x16, -0x76a32842);
            _0x3894d9 = _0xaa05ae(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0xc], 0x7, 0x6b901122);
            _0x17bf86 = _0xaa05ae(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0xd], 0xc, -0x2678e6d);
            _0x545346 = _0xaa05ae(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xe], 0x11, -0x5986bc72);
            _0x8d34ed = _0xaa05ae(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0xf], 0x16, 0x49b40821);
            _0x3894d9 = _0x5a5634(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x1], 0x5, -0x9e1da9e);
            _0x17bf86 = _0x5a5634(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x6], 0x9, -0x3fbf4cc0);
            _0x545346 = _0x5a5634(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xb], 0xe, 0x265e5a51);
            _0x8d34ed = _0x5a5634(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127], 0x14, -0x16493856);
            _0x3894d9 = _0x5a5634(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x5], 0x5, -0x29d0efa3);
            _0x17bf86 = _0x5a5634(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0xa], 0x9, 0x2441453);
            _0x545346 = _0x5a5634(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xf], 0xe, -0x275e197f);
            _0x8d34ed = _0x5a5634(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x4], 0x14, -0x182c0438);
            _0x3894d9 = _0x5a5634(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x9], 0x5, 0x21e1cde6);
            _0x17bf86 = _0x5a5634(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0xe], 0x9, -0x3cc8f82a);
            _0x545346 = _0x5a5634(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x3], 0xe, -0xb2af279);
            _0x8d34ed = _0x5a5634(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x8], 0x14, 0x455a14ed);
            _0x3894d9 = _0x5a5634(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0xd], 0x5, -0x561c16fb);
            _0x17bf86 = _0x5a5634(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x2], 0x9, -0x3105c08);
            _0x545346 = _0x5a5634(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x7], 0xe, 0x676f02d9);
            _0x8d34ed = _0x5a5634(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0xc], 0x14, -0x72d5b376);
            _0x3894d9 = _0x5d8807(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x5], 0x4, -0x5c6be);
            _0x17bf86 = _0x5d8807(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x8], 0xb, -0x788e097f);
            _0x545346 = _0x5d8807(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xb], 0x10, 0x6d9d6122);
            _0x8d34ed = _0x5d8807(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0xe], 0x17, -0x21ac7f4);
            _0x3894d9 = _0x5d8807(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x1], 0x4, -0x5b4115bc);
            _0x17bf86 = _0x5d8807(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x4], 0xb, 0x4bdecfa9);
            _0x545346 = _0x5d8807(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x7], 0x10, -0x944b4a0);
            _0x8d34ed = _0x5d8807(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0xa], 0x17, -0x41404390);
            _0x3894d9 = _0x5d8807(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0xd], 0x4, 0x289b7ec6);
            _0x17bf86 = _0x5d8807(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127], 0xb, -0x155ed806);
            _0x545346 = _0x5d8807(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x3], 0x10, -0x2b10cf7b);
            _0x8d34ed = _0x5d8807(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x6], 0x17, 0x4881d05);
            _0x3894d9 = _0x5d8807(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x9], 0x4, -0x262b2fc7);
            _0x17bf86 = _0x5d8807(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0xc], 0xb, -0x1924661b);
            _0x545346 = _0x5d8807(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xf], 0x10, 0x1fa27cf8);
            _0x8d34ed = _0x5d8807(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x2], 0x17, -0x3b53a99b);
            _0x3894d9 = _0x318283(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127], 0x6, -0xbd6ddbc);
            _0x17bf86 = _0x318283(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x7], 0xa, 0x432aff97);
            _0x545346 = _0x318283(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xe], 0xf, -0x546bdc59);
            _0x8d34ed = _0x318283(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x5], 0x15, -0x36c5fc7);
            _0x3894d9 = _0x318283(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0xc], 0x6, 0x655b59c3);
            _0x17bf86 = _0x318283(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0x3], 0xa, -0x70f3336e);
            _0x545346 = _0x318283(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0xa], 0xf, -0x100b83);
            _0x8d34ed = _0x318283(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x1], 0x15, -0x7a7ba22f);
            _0x3894d9 = _0x318283(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x8], 0x6, 0x6fa87e4f);
            _0x17bf86 = _0x318283(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0xf], 0xa, -0x1d31920);
            _0x545346 = _0x318283(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x6], 0xf, -0x5cfebcec);
            _0x8d34ed = _0x318283(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0xd], 0x15, 0x4e0811a1);
            _0x3894d9 = _0x318283(_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86, _0x514574[_0x406127 + 0x4], 0x6, -0x8ac817e);
            _0x17bf86 = _0x318283(_0x17bf86, _0x3894d9, _0x8d34ed, _0x545346, _0x514574[_0x406127 + 0xb], 0xa, -0x42c50dcb);
            _0x545346 = _0x318283(_0x545346, _0x17bf86, _0x3894d9, _0x8d34ed, _0x514574[_0x406127 + 0x2], 0xf, 0x2ad7d2bb);
            _0x8d34ed = _0x318283(_0x8d34ed, _0x545346, _0x17bf86, _0x3894d9, _0x514574[_0x406127 + 0x9], 0x15, -0x14792c6f);
            _0x3894d9 = _0xf848b6(_0x3894d9, _0x103546);
            _0x8d34ed = _0xf848b6(_0x8d34ed, _0x896dff);
            _0x545346 = _0xf848b6(_0x545346, _0x5d8d82);
            _0x17bf86 = _0xf848b6(_0x17bf86, _0x5b6717);
        }
        return [_0x3894d9, _0x8d34ed, _0x545346, _0x17bf86];
    }
    function _0x1b432e(_0x318f27) {
        var _0x213d40;
        var _0x5ee7f7 = '';
        var _0x56884a = _0x318f27[_0x3551('0x0')] * 0x20;
        for (_0x213d40 = 0x0; _0x213d40 < _0x56884a; _0x213d40 += 0x8) {
            _0x5ee7f7 += String[_0x3551('0x1')](_0x318f27[_0x213d40 >> 0x5] >>> _0x213d40 % 0x20 & 0xff);
        }
        return _0x5ee7f7;
    }
    function _0x10ffc6(_0x2ece02) {
        var _0x43844c;
        var _0x116949 = [];
        _0x116949[(_0x2ece02[_0x3551('0x0')] >> 0x2) - 0x1] = undefined;
        for (_0x43844c = 0x0; _0x43844c < _0x116949['length']; _0x43844c += 0x1) {
            _0x116949[_0x43844c] = 0x0;
        }
        var _0x26257e = _0x2ece02[_0x3551('0x0')] * 0x8;
        for (_0x43844c = 0x0; _0x43844c < _0x26257e; _0x43844c += 0x8) {
            _0x116949[_0x43844c >> 0x5] |= (_0x2ece02['charCodeAt'](_0x43844c / 0x8) & 0xff) << _0x43844c % 0x20;
        }
        return _0x116949;
    }
    function _0x3e2628(_0x32569f) {
        return _0x1b432e(_0x45e748(_0x10ffc6(_0x32569f), _0x32569f[_0x3551('0x0')] * 0x8));
    }
    function _0x56a776(_0xcb72a2, _0x52982d) {
        var _0x248c33;
        var _0x21838a = _0x10ffc6(_0xcb72a2);
        var _0x3e451e = [];
        var _0x4e5594 = [];
        var _0x350fc7;
        _0x3e451e[0xf] = _0x4e5594[0xf] = undefined;
        if (_0x21838a[_0x3551('0x0')] > 0x10) {
            _0x21838a = _0x45e748(_0x21838a, _0xcb72a2[_0x3551('0x0')] * 0x8);
        }
        for (_0x248c33 = 0x0; _0x248c33 < 0x10; _0x248c33 += 0x1) {
            _0x3e451e[_0x248c33] = _0x21838a[_0x248c33] ^ 0x36363636;
            _0x4e5594[_0x248c33] = _0x21838a[_0x248c33] ^ 0x5c5c5c5c;
        }
        _0x350fc7 = _0x45e748(_0x3e451e[_0x3551('0x2')](_0x10ffc6(_0x52982d)), 0x200 + _0x52982d[_0x3551('0x0')] * 0x8);
        return _0x1b432e(_0x45e748(_0x4e5594[_0x3551('0x2')](_0x350fc7), 0x200 + 0x80));
    }
    function _0x4476e5(_0x5e7bd4) {
        var _0x25745a = '0123456789abcdef';
        var _0x1bb4fd = '';
        var _0x5a1951;
        var _0xf4d402;
        for (_0xf4d402 = 0x0; _0xf4d402 < _0x5e7bd4[_0x3551('0x0')]; _0xf4d402 += 0x1) {
            _0x5a1951 = _0x5e7bd4['charCodeAt'](_0xf4d402);
            _0x1bb4fd += _0x25745a[_0x3551('0x3')](_0x5a1951 >>> 0x4 & 0xf) + _0x25745a[_0x3551('0x3')](_0x5a1951 & 0xf);
        }
        return _0x1bb4fd;
    }
    function _0x37d7f1(_0x3321b5) {
        return unescape(encodeURIComponent(_0x3321b5));
    }
    function _0x4897ab(_0x1f3964) {
        return _0x3e2628(_0x37d7f1(_0x1f3964));
    }
    function _0x5c9998(_0x42d437) {
        return _0x4476e5(_0x4897ab(_0x42d437));
    }
    function _0x413677(_0x32cd7a, _0x5f3088) {
        return _0x56a776(_0x37d7f1(_0x32cd7a), _0x37d7f1(_0x5f3088));
    }
    function _0x15476b(_0x300820, _0x5861df) {
        return _0x4476e5(_0x413677(_0x300820, _0x5861df));
    }
    function _0x1c7889(_0x109e42, _0x434a83, _0x3c243f) {
        if (!_0x434a83) {
            if (!_0x3c243f) {
                return _0x5c9998(_0x109e42);
            }
            return _0x4897ab(_0x109e42);
        }
        if (!_0x3c243f) {
            return _0x15476b(_0x434a83, _0x109e42);
        }
        return _0x413677(_0x434a83, _0x109e42);
    }
    function _0x515c70(_0x503154) {
        var _0xacc7f7, _0x126261 = new RegExp(_0x3551('0x5') + _0x503154 + _0x3551('0x6'));
        if (_0xacc7f7 = document[_0x3551('0x7')][_0x3551('0x8')](_0x126261))
            return unescape(_0xacc7f7[0x2]);
        else
            return '';
    }
    function _0x89ea42() {
        var _0x150c4d = new Date();
        var _0x4e6d5d = Date.parse(_0x150c4d);
        return _0x4e6d5d / 0x3e8;
    }
    function _0x55bae5(_0x36a60f, _0x37fe42, _0x903bc9) {
        var _0x265f92 = _0x36a60f['substring'](0x0, _0x903bc9);
        var _0x3d1b53 = _0x36a60f['substring'](_0x903bc9, 0x20);
        return _0x265f92 + _0x37fe42 + _0x3d1b53;
    }
    function _0x39990b(_0x1472c1) {
        var _0x417e56 = '';
        for (var _0x5521d9 = _0x1472c1[_0x3551('0x0')] - 0x1; _0x5521d9 >= 0x0; _0x5521d9--) {
            _0x417e56 += _0x1472c1[_0x3551('0x3')](_0x5521d9);
        }
        return _0x417e56;
    }
    var _0x1bd82b = _0x3551('0x4');
    var _0x4bef56 = _0x515c70(_0x3551('0x39'));
    var _0x5c6712 = _0x1c7889(_0x1bd82b + _0x4bef56);
    var _0x597b06 = _0x89ea42();
    var _0x179ec1 = _0x55bae5(_0x5c6712, _0x597b06, 0x10);
    var _0x32e0d2 = _0x39990b(_0x179ec1);
    return _0x32e0d2
}

jt = function(aesKey, originalData, u) {
    var e = {deviceType: 1}
      , t = "".concat(JSON.stringify(e)).concat(u).concat(JSON.stringify(originalData))
      , t = (t = t, null === (t = CryptoJS.SHA256(t).toString()) || void 0 === t ? void 0 : t.toUpperCase());

    return Rt(JSON.stringify({
        originHeader: JSON.stringify(e),
        code: t
    }), aesKey)
}

Rt = function (t, aesKey) {
    var Ot = CryptoJS.enc.Utf8.parse("c558Gq0YQK2QUlMc"),
        Dt = CryptoJS.enc.Utf8.parse(aesKey),
        t = CryptoJS.enc.Utf8.parse(t);
    t = CryptoJS.AES.encrypt(t, Dt, {
        iv: Ot,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return t.toString()
};

It = function(t, aesKey) {
    var Ot = CryptoJS.enc.Utf8.parse("c558Gq0YQK2QUlMc"),
    Dt = CryptoJS.enc.Utf8.parse(aesKey);
    t = CryptoJS.AES.decrypt(t, Dt, {
        iv: Ot,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString(CryptoJS.enc.Utf8);
    try {
        t = JSON.parse(t)
    } catch (t) {}
    return t
}

function E(t) {
    for (var b = [], w = 0; w < 256; ++w)
            b[w] = (w + 256).toString(16).substr(1);
    var T = new Uint8Array(16);
    return function(t) {
        for (var e = [], n = 0; n < t.length; n++)
            e.push(b[t[n]]);
        return e.join("")
    }(getRandomValues(T)).substr(0, t)
}