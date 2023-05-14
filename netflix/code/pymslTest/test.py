import pymsl
email="k8q238@163.com"
password="asd558"
user_auth_data = {
     'scheme': 'EMAIL_PASSWORD',
        'authdata': {
       'email': email,
      'password': password
    }
    }
client = pymsl.MslClient(user_auth_data)
client.load_manifest(80092521)
