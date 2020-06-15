# 1.导包
import threading
import socket


# 创建服务端类
class HttpWebServer(object):
    def __init__(self):
        # 2.创建套接字
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 3.设置端口复用
        self.server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 4.绑定ip和端口
        self.server_conn.bind(('', 11111))
        # 5.设置监听套接字
        self.server_conn.listen(128)

    def start(self):
        while True:
            # 6.等待客户端的链接
            new_socket, client_ip_port = self.server_conn.accept()
            # 6.1 创建线程
            t1 = threading.Thread(target=self.handle_client_server, args=(new_socket,client_ip_port))
            # 6.2 启动线程
            t1.start()

    @staticmethod
    def handle_client_server(new_socket, client_ip_port):
        print(f"客户端{client_ip_port}链接了")
        # 7.接收客户端发送的数据
        client_data = new_socket.recv(4096)
        if len(client_data) == 0:
            print('客户端关闭了')
            new_socket.close()
            return
        # 组织发送给客户端的数据
        # 7.1 读取客户端请求的资源文件吗
        client_file_name = client_data.decode().split(' ', 2)[1]
        print(client_file_name)
        # 7.2 判断用胡请求的文件名是否为空
        if client_file_name == '/':
            # 返回首页的数据
            client_file_name = '/5.16/static/index.html'
        try:
            # 7.3组织响应行
            response_line = 'HTTP/1.1 200 OK\r\n'
            with open('./5.16/static/' + client_file_name, 'rb') as f:
                response_data = f.read()
        except FileNotFoundError:
            response_line = 'HTTP/1.1 404 Not File Found\r\n'
            with open('./5.16/static/error.html', 'rb') as f:
                response_data = f.read()
        # 7.4 组织响应头
        response_header = 'Server:haha\r\nName:python\r\n'
        # 7.5 组装要发送的数据
        response = (response_line + response_header + '\r\n').encode() + response_data
        # 8.给客户端发送数据
        new_socket.send(response)
        # 9.关闭通信套接字
        new_socket.close()

    def __del__(self):
        # 10.关闭链接套接字
        self.server_conn.close()

if __name__ == '__main__':
    # 创建服务端对象
    server = HttpWebServer()
    server.start()

