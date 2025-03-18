import socket
import json
from rsa import RSA

rsa = RSA()


class Client:

    def __init__(self, server_host="127.0.0.1", server_port=8888, client_port=8904):
        self.server_host = server_host
        self.server_port = server_port
        self.client_port = client_port
        self.client_socket = None
        self.private_key_pem, self.public_key_pem, self.private_key, self.public_key = (
            rsa.generate_keys().values()
        )
        print(f"[Cliente] Chave pública cliente: {self.public_key_pem}")
        print(f"[Cliente] Chave privada cliente: {self.private_key_pem}")

    def connect_to_server(self):
        """Conecta ao servidor de troca de chaves"""
        try:
            print("[Cliente] Conectando ao servidor")
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

            if self.client_port != 0:
                self.client_socket.bind(("0.0.0.0", self.client_port))

            self.client_socket.connect((self.server_host, self.server_port))
            actual_port = self.client_socket.getsockname()[1]
            print(
                f"Conectado ao servidor {self.server_host}:{
                    self.server_port} a partir da porta {actual_port}"
            )
            return True

        except Exception as e:
            print(f"[Cliente] Erro ao conectar ao servidor: {str(e)}")
            return False

    def register(self):
        """Registra o cliente no servidor e obtém a chave pública do servidor"""
        message = {
            "public_key": self.public_key_pem,
        }

        response = self.send_message(message)
        if response and response.get("status") == "success":
            encrypted_message = response.get("message")
            print(
                f"[Cliente] Mensagem criptografada recebida: {
                    encrypted_message}"
            )
            print(
                f"[Cliente] Descriptografando mensagem com chave privada: {
                    self.private_key_pem}"
            )
            print(
                f"[Cliente] Mensagem descriptografada: {
                    rsa.decrypt_message(encrypted_message, self.private_key)}"
            )
            self.server_public_key = response.get("server_public_key")
            return True
        else:
            error_msg = (
                response.get(
                    "message") if response else "Sem resposta do servidor"
            )
            print(f"Falha no registro: {error_msg}")
            return False

    def send_message(self, message):
        """Envia mensagem para o servidor e retorna a resposta"""
        if not self.client_socket:
            print("[Cliente] Não conectado ao servidor")
            return None

        try:
            self.client_socket.send(
                message["public_key"],
            )
            response_data = self.client_socket.recv(4096)
            response = json.loads(response_data.decode("utf-8"))
            return response

        except Exception as e:
            print(e)
            print(f"[Clinete] Erro na comunicação com o servidor: {str(e)}")
            return None

    def close(self):
        """Fecha a conexão com o servidor"""
        if self.client_socket:
            self.client_socket.close()
            print("[Client] Conexão encerrada")
