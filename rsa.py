from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

PUBLIC_EXPONENT = 65537
KEY_SIZE = 2048


class RSA:
    def generate_keys(self):
        """Gera 4 chaves 2 públicas uma serialiazada outra não e 2 privas 1 serializada outra não"""
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return {
            "private_key_pem": private_pem,
            "public_key_pem": public_pem,
            "private_key": private_key,
            "public_key": public_key,
        }

    def encrypt_message(self, message, public_key):
        """Criptografa uma mensagem usando a chave pública do destinatário"""
        if not public_key:
            return {"error": "No public key received"}

        encrypted_message = public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return base64.b64encode(encrypted_message).decode("utf-8")

    def decrypt_message(self, message, private_key):
        """descriptografa uma mensagem com uma chave privada recebida"""
        print(message)
        encrypted = base64.b64decode(message)

        plaintext = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        ).decode("utf-8")
        return plaintext

    def load_pem_public_key(self, public_key_pem):
        """Retorna a chave pública desserializada através da serializada"""
        return serialization.load_pem_public_key(public_key_pem)
