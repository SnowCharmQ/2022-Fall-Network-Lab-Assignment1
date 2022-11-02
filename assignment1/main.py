import os
import json
import random
import string
from typing import *
import config
import mimetypes
from framework import HTTPServer, HTTPRequest, HTTPResponse


def random_string(length=20):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def default_handler(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    response.status_code, response.reason = 404, 'Not Found'
    print(f"calling default handler for url {request.request_target}")


def task2_data_handler(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO(F): Task 2: Serve static content based on request URL (20%)
    if request.method == "POST":
        response.status_code, response.reason = 405, "Method Not Allowed"
        return
    target = request.request_target[0:]
    cwd = os.getcwd()
    path = os.path.join(cwd, target.replace("/", "\\")[1:])
    try:
        file = open(path, mode='rb')
    except FileNotFoundError:
        response.status_code, response.reason = 404, 'Not Found'
        return
    path = path.split("\\")[-1]
    content_type = mimetypes.guess_type(path)
    response.add_header("Content-Type", content_type[0])
    content = file.read()
    response.add_header("Content-Length", str(len(content)))
    response.status_code, response.reason, response.body = 200, "OK", content


def task3_json_handler(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO(F): Task 3: Handle POST Request (20%)
    response.status_code, response.reason = 200, 'OK'
    if request.method == 'POST':
        binary_data = request.read_message_body()
        obj = json.loads(binary_data)
        # TODO(F): Task 3: Store data when POST
        server.task3_data = obj['data']
        response.status_code, response.reason = 200, "OK"
    else:
        obj = {'data': server.task3_data}
        return_binary = json.dumps(obj).encode()
        content_type = "application/json"
        content_length = str(len(return_binary))
        response.add_header("Content-Type", content_type)
        response.add_header("Content-Length", content_length)
        response.status_code, response.reason, response.body = 200, "OK", return_binary


def task4_url_redirection(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 4: HTTP 301 & 302: URL Redirection (10%)
    pass


def task5_test_html(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    response.status_code, response.reason = 200, 'OK'
    with open("task5.html", "rb") as f:
        response.body = f.read()


def task5_cookie_login(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 1 Login Authorization
    obj = json.loads(request.read_message_body())
    if obj["username"] == 'admin' and obj['password'] == 'admin':
        pass
    else:
        pass


def task5_cookie_getimage(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 2 Access Protected Resources
    pass


def task5_session_login(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 1 Login Authorization
    obj = json.loads(request.read_message_body())
    if obj["username"] == 'admin' and obj['password'] == 'admin':
        session_key = random_string()
        while session_key in server.session:
            session_key = random_string()
        pass
    else:
        response.status_code, response.reason = 403, 'Forbidden'


def task5_session_getimage(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 2 Access Protected Resources
    pass


# TODO(F): Change this to your student ID, otherwise you may lost all of your points
YOUR_STUDENT_ID = 12013006

http_server = HTTPServer(config.LISTEN_PORT)
http_server.register_handler("/", default_handler)
# Register your handler here!
http_server.register_handler("/data", task2_data_handler, allowed_methods=['GET', 'HEAD'])
http_server.register_handler("/post", task3_json_handler, allowed_methods=['GET', 'HEAD', 'POST'])
http_server.register_handler("/redirect", task4_url_redirection, allowed_methods=['GET', 'HEAD'])
# Task 5: Cookie
http_server.register_handler("/api/login", task5_cookie_login, allowed_methods=['POST'])
http_server.register_handler("/api/getimage", task5_cookie_getimage, allowed_methods=['GET', 'HEAD'])
# Task 5: Session
http_server.register_handler("/apiv2/login", task5_session_login, allowed_methods=['POST'])
http_server.register_handler("/apiv2/getimage", task5_session_getimage, allowed_methods=['GET', 'HEAD'])

# Only for browser test
http_server.register_handler("/api/test", task5_test_html, allowed_methods=['GET'])
http_server.register_handler("/apiv2/test", task5_test_html, allowed_methods=['GET'])


def start_server():
    try:
        http_server.run()
    except Exception as e:
        http_server.listen_socket.close()
        print(e)


if __name__ == '__main__':
    start_server()
