import socket
import threading
import json

from rsa import RSA

rsa = RSA()


class Server:
    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key_pem, self.public_key_pem, self.private_key, self.public_key = (
            rsa.generate_keys().values()
        )

    def start(self):
        """Inicia o servidor"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[Server] Servidor iniciado em {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[Server] Nova conexão de {client_address}")

                client_thread = threading.Thread(
                    target=self.handle_client, args=(
                        client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            print("[Server] Encerrando servidor...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        """Manipula comunicação com um cliente"""
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break

                try:
                    client_public_key_pem = data
                    response = self.register_client(client_public_key_pem)

                    client_socket.send(json.dumps(response).encode("utf-8"))

                except json.JSONDecodeError:
                    print(
                        f"[Server] Erro ao decodificar mensagem de {
                            client_address}"
                    )
                    client_socket.send(
                        json.dumps(
                            {"status": "error", "message": "Formato JSON inválido"}
                        ).encode("utf-8")
                    )

        except Exception as e:
            print(
                f"[Server] Erro ao lidar com cliente {
                    client_address}: {str(e)}"
            )

        finally:
            client_socket.close()
            print(f"[Server] Conexão encerrada com {client_address}")

    def register_client(self, public_key_pem):
        """Registra um novo cliente e sua chave pública"""
        client_public_key = rsa.load_pem_public_key(public_key_pem)
        if not client_public_key:
            return {
                "status": "error",
                "message": "public key is required",
            }
        message = "teste"
        print(
            f"[Server] Encriptando a mensagem: {
                message} usando a chave {public_key_pem}"
        )
        return {
            "status": "success",
            "message": rsa.encrypt_message(message, client_public_key),
        }
