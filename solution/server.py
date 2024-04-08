from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
pedidos=[
    {
        "client":"Juan Perez",
        "status": "Pendiente",
        "payment": "Tarjeta de Credito",
        "shipping":10.0,
        "order_type":"Digital"
    },
]
    

class RestRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_p= urlparse(self.path)
        query_params = parse_qs(parsed_p.query)
        if parsed_p.path=="/orders":
            if "status" in query_params:
                status = query_params["status"][0]
                pedidos_estatus=next(
                    pedido for pedido in pedidos if pedidos["status"]==status
                )
                if pedidos_estatus:
                    self.send_response(201)
                    self.send_header("", "")
                    self.end_headers()
                    self.wfile.write(json.dumps(pedidos_estatus).encode("utf-8"))
                else:
                    self.send_response(204)
                    self.send_header("", "")
                    self.end_headers()
                    self.wfile.write(json.dumps("no se encontro status").encode("utf-8"))
                            

            else: 
                self.send_response(200)
                self.send_header("", "")
                self.end_headers()
                self.wfile.write(json.dumps(pedidos).encode("utf-8"))   
        else:
            self.send_response(404)
            self.send_header("", "")
            self.end_headers()
            self.wfile.write(json.dumps("ruta no encontrada").encode("utf-8"))    
        

def run_server():
    try:
        server_adress=('', 8000)
        httpd=HTTPServer(server_adress, RestRequestHandler)
        print("levantando servidor web/")
        httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("apagando el servidor")
        httpd.socket.close()

if __name__=="__main__":
    run_server()
      

