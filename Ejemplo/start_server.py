import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.getcwd()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor sirviendo en el puerto {PORT}")
        print(f"Abre tu navegador en: http://localhost:{PORT}")
        print("Presiona Ctrl+C para detener el servidor.")
        httpd.serve_forever()
except OSError as e:
    print(f"Error al iniciar el servidor: {e}")
    print(f"Es probable que el puerto {PORT} ya esté en uso o se requieran permisos.")
except KeyboardInterrupt:
    print("\nServidor detenido por el usuario.")
