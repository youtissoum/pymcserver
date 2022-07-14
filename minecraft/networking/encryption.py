from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives import serialization

def load_der(pub_key: rsa.RSAPublicKey):
    return pub_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)

def rsa_decrypt(value, priv_key: rsa.RSAPrivateKey):
    return priv_key.decrypt(value, PKCS1v15())

def generate_pub_and_priv_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    priv_key = rsa.generate_private_key(
        public_exponent=65537, 
        key_size=1024
    )
    pub_key = priv_key.public_key()
    return((priv_key, pub_key))