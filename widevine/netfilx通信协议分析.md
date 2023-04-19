## netfilx通信协议分析

### login1

#### url

~~~
https://www.netflix.com/msl/playapi/cadmium/licensedmanifest/1?reqAttempt=1&reqName=prefetch/licensedManifest&clienttype=akira&uiversion=v422d49b0&browsername=edgeoss&browserversion=86.0.622&osname=windows&osversion=10.0
~~~

#### type

**post**

#### body

##### 创建RSA秘钥

~~~python
self.rsa_key = RSA.generate(2048)
~~~

##### 生成msl_header

~~~json
{
    "capabilities":{
        "languages":[

        ],
        "compressionalgos":[
            "LZW"
        ]
    },
    "renewable":true,
    "messageid":4419143807642995,
    "keyrequestdata":[
        {
            "scheme":"ASYMMETRIC_WRAPPED",
            "keydata":{
                "publickey":"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsDUMtC5v9+vV3JVhVG7wHi6BXxVJDUB3X1iUeY6z936RVnaC4eXtG2abFwrlxrFMdGrzk27iw6yGNRILnjyC8UWfBfzolSLJa4Ae/RK7uW0LRJgJ/9dbIOSal/AO2DkMivuOuly6W+1+JoE2uffULhoQCvsOmk+yPNVR1/cX9s9K9EP8CRs1QUG3g33na/zogdbEKleV3GPZHyMlHtUoNmDKnkYWdeFwCzXzrkUjst8pFR3tmFzDLgW6p6IUh6VZJaoWGKmO08OOjjLcMm7McYW6SBQwE5ZrohgRHwLBTBWSAOcfu3Omih8c8cPJOVVDOmO8Vbv3NtNDSMe6oFI/xwIDAQAB",
                "mechanism":"JWK_RSA",
                "keypairid":"rsaKeypairId"
            }
        }
    ]
}
~~~

**messageid**

~~~python
self.current_message_id = self.rndm.randint(0, pow(2, 52))
~~~

**publickey**

~~~python
 public_key = base64.standard_b64encode(self.rsa_key.publickey().exportKey(format='DER')).decode('utf-8')
~~~

##### 生成msl_end

~~~json
{
    "sequencenumber":1,
    "messageid":4419143807642995,
    "endofmsg":true,
    "compressionalgo":"LZW",
    "data":""
}
~~~

~~~json
{"entityauthdata": {"scheme": "NONE", "authdata": {"identity": "NFCDIE-03-J7K735E5XQ17EHRLGQQ8CVWPD5AMEP"}}, "headerdata": "eyJjYXBhYmlsaXRpZXMiOiB7Imxhbmd1YWdlcyI6IFtdLCAiY29tcHJlc3Npb25hbGdvcyI6IFsiTFpXIl19LCAicmVuZXdhYmxlIjogdHJ1ZSwgIm1lc3NhZ2VpZCI6IDQ0MTkxNDM4MDc2NDI5OTUsICJrZXlyZXF1ZXN0ZGF0YSI6IFt7InNjaGVtZSI6ICJBU1lNTUVUUklDX1dSQVBQRUQiLCAia2V5ZGF0YSI6IHsicHVibGlja2V5IjogIk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBc0RVTXRDNXY5K3ZWM0pWaFZHN3dIaTZCWHhWSkRVQjNYMWlVZVk2ejkzNlJWbmFDNGVYdEcyYWJGd3JseHJGTWRHcnprMjdpdzZ5R05SSUxuanlDOFVXZkJmem9sU0xKYTRBZS9SSzd1VzBMUkpnSi85ZGJJT1NhbC9BTzJEa01pdnVPdWx5NlcrMStKb0UydWZmVUxob1FDdnNPbWsreVBOVlIxL2NYOXM5SzlFUDhDUnMxUVVHM2czM25hL3pvZ2RiRUtsZVYzR1BaSHlNbEh0VW9ObURLbmtZV2RlRndDelh6cmtVanN0OHBGUjN0bUZ6RExnVzZwNklVaDZWWkphb1dHS21PMDhPT2pqTGNNbTdNY1lXNlNCUXdFNVpyb2hnUkh3TEJUQldTQU9jZnUzT21paDhjOGNQSk9WVkRPbU84VmJ2M050TkRTTWU2b0ZJL3h3SURBUUFCIiwgIm1lY2hhbmlzbSI6ICJKV0tfUlNBIiwgImtleXBhaXJpZCI6ICJyc2FLZXlwYWlySWQifX1dfQ==", "signature": ""}{"payload": "eyJzZXF1ZW5jZW51bWJlciI6IDEsICJtZXNzYWdlaWQiOiA0NDE5MTQzODA3NjQyOTk1LCAiZW5kb2Ztc2ciOiB0cnVlLCAiY29tcHJlc3Npb25hbGdvIjogIkxaVyIsICJkYXRhIjogIiJ9", "signature": ""}
~~~

**headerdata**

~~~python
base64.standard_b64encode(msl_header.encode('utf-8')).decode('utf-8')
~~~

**payload**

~~~
base64.standard_b64encode(msl_end.encode('utf-8')).decode('utf-8')
~~~

#### response

