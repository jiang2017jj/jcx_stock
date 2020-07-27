import base64
import binascii
from hashlib import md5
from pyDes import des, PAD_PKCS5
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


def my_rsa(data_1):
    '''
    加密一般有对称加密，非对称加密
    对称加密，就是加密和解密用同一个密钥，DES，AES
    非对称加密，就是加密和解密不用同一个密钥，RSA
    :return:
    '''
    # 生成密钥对
    key_pair = RSA.generate(1024)

    # 导入公钥
    pub_key = RSA.importKey(key_pair.publickey().exportKey())
    # 导入私钥
    pri_key = RSA.importKey(key_pair.exportKey())

    #对message1进行加密
    data = pub_key.encrypt(data_1.encode(),None)
    print(data)

    # 对加密数据进行BASE64编码
    message2 = base64.b64encode(data[0])
    print(message2)

    # 对加密数据进行BASE64解码
    data = base64.b64decode(message2)
    print(data)

    # 解密数据
    message3 = pri_key.decrypt(data)
    print(message3.decode())


def my_aes(data):
    # AES加密的密钥必须是32位或者16位或者24位
    # aes_key = "12345678901234567890123456789012"

    # 这样处理下也是32位
    aes_key = md5(b'12345678').hexdigest()
    print(aes_key)

    BS = AES.block_size

    cipher = AES.new(aes_key)

    # 加密
    pad = lambda s:s+(BS-len(s)%BS)*chr(BS-len(s)%BS)
    message1 = cipher.encrypt(pad(data))
    print(message1)
    result1 = base64.b64encode(message1)
    print(result1)

    # 解密
    unpad = lambda s:s[0:-s[-1]]
    result2 = base64.b64decode(result1)
    message2 = cipher.decrypt(result2)
    print(message2)

# https://www.cnblogs.com/gqv2009/p/12681996.html
# des加密解密
def my_des3(data):
    des_key = '12346789'
    iv = des_key

    # 加密解密需要用到的
    k = des(des_key,iv,pad=None,padmode=PAD_PKCS5)

    # 加密
    en = k.encrypt(data,padmode=PAD_PKCS5)
    print(binascii.b2a_hex(en))

    # 解密
    de = k.decrypt(binascii.b2a_hex(en),padmode=PAD_PKCS5)
    print(de)



if __name__=="__main__":
    data = "{'token':'123456', 'name':'Victor','age':1, 'gender':1, 'id':123, 'company':'injiajia.com'}"
    my_rsa(data)
    print()
    my_aes(data)
    print()
    my_des3(data)