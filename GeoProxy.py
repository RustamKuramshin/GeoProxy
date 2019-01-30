#!/usr/bin/python3

import socket

import select

import time

import sys

buffer_size = 4096
delay = 0.0001
forward_to = ('193.193.165.165', 20987)


class Forward:

    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):

        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            print(e)
            return False


class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):

        self.input_list.append(self.server)
        while True:

            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])

            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break
                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):

        forward = Forward().start(forward_to[0], forward_to[1])
        clientsock, clientaddr = self.server.accept()
        if forward:
            print(f"{clientaddr} подключился")
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            print("Не удается установить соединение с удаленным сервером.", )
            print(f"Закрытие соединения со стороны клиента {clientaddr}")
            clientsock.close()

    def on_close(self):

        print(f"{self.s.getpeername()} отключился")
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):

        data = self.data
        print(data)
        self.channel[self.s].send(data)


if __name__ == '__main__':

    server = TheServer('192.168.61.98', 35245)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print("Нажмите Ctrl + C для остановки сервера")
        sys.exit(1)
