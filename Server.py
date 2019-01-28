#!/usr/bin/python3

import socket
import libscrc
import binascii

SERVER_ADDRESS = ('192.168.61.98', 35245)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)
print('TCP-сервер запущен, для остановки нажмите Ctrl+C')

while True:
    connection, address = server_socket.accept()
    print("Новое соединение от {address}".format(address=address))
    data = connection.recv(4096)
    print(data.hex())

    crc_slice = data[-2:]
    crc16 = libscrc.modbus(data[:-2]).to_bytes(2, byteorder='little')
    confirmPackage = b'\x02' + data[-2:]
    imei = data[4:13].decode()
    print('Длина данных прикладного уровня: ' + str(len(data)))
    print(f'Контрольная сумма из пакета {crc_slice}')
    print(f'Контрольная сумма вычисленная {crc16}')
    print('Контрольные суммы: ' + ('good' if crc16 == crc_slice else 'bad'))
    print(f'Пакет подтверждения: {confirmPackage}')
    print('Контрольная сумма (hexlify): {}'.format(binascii.hexlify(crc16)))
    print(f'Идентификатор локаруса (IMEI): {imei}')
    connection.send(confirmPackage)
    connection.close()
