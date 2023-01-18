from Crypto.Cipher import AES
import base64

HashKey="pwFHCqoQZGmho4w6"
HashIV="EkRm7iFT261dpevs"

class AESEncrypter(object): # 加解密
    def __init__(self,key,iv):
        self.key =key.encode("utf8")
        self.iv =iv.encode("utf8")

    def _pad(self, text):
        text_length = len(text)
        padding_len = AES.block_size - int(text_length % AES.block_size)
        if padding_len == 0:
            padding_len = AES.block_size

        t2 = chr(padding_len) * padding_len
        t2 = t2.encode('utf8')
        # print('text ', type(text), text)
        # print('t2 ', type(t2), t2)
        t3 = text + t2
        return t3

    def _unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, raw):
        raw = raw.encode('utf8')
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(raw)
        return base64.b64encode(encrypted).decode('utf8')

    def decrypt(self, enc):
        enc = enc.encode('utf8')
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(enc)
        return self._unpad(decrypted.decode('utf8'))

class AESTool:
    def __init__(self):
        self.key = HashKey.encode('utf-8')
        self.iv = HashIV.encode('utf-8')

    def pkcs7padding(self, text):
        """
        加密格式:PKCS7
        """
        bs = 16 # 長度16
        length = len(text) # 243
        bytes_length = len(text.encode('utf-8')) # 243
        padding_size = length if (bytes_length == length) else bytes_length
        # padding_size % bs = 3
        padding = bs - padding_size % bs
        # padding = 13
        padding_text = chr(padding) * padding # chr 編碼轉字符
        self.coding = chr(padding)

        return text + padding_text

    def aes_encrypt(self, content):
        """
        AES加密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 整理字串
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def aes_decrypt(self, content):
        """
        AES解密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = base64.b64decode(content)
        text = cipher.decrypt(content).decode('utf-8')
        return self.pkcs7padding(text)

# aes_tool = AESTool()
# url_encodeStr = 'MerchantID=3002607&RqHeader=Timestamp&Data=enter+your+data'
# encrypt_str = aes_tool.aes_encrypt(url_encodeStr)
# print(encrypt_str)
