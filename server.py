from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import datetime
import pytz

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Устанавливаем московский часовой пояс
            msk_timezone = pytz.timezone('Europe/Moscow')
            current_time = datetime.datetime.now(msk_timezone)

            # Создаем динамическое сообщение в зависимости от времени суток
            if current_time.time() < datetime.time(12):
                message = "Good morning! Server is healthy."
            elif current_time.time() < datetime.time(18):
                message = "Good afternoon! Server is healthy."
            else:
                message = "Good evening! Server is healthy."

            response = {
                'status': '200 OK',
                'message': message,
                'timestamp': current_time.isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=HealthCheckHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
