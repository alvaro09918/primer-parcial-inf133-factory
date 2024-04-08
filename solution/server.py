from http.server import HTTPServer, BaseHTTPRequestHandler
import json

pedidos = {}

class Pedido:
    def __init__(self, client, status, payment,shipping,order_type):
        self.order_type=order_type
        self.client=client
        self.status=status
        self.payment=payment
        self.shipping=shipping
        
class Fisico(Pedido):
    def __init__(self, client, status, payment,shipping):
        super.__init__("fisico",client, status, payment,shipping) 

class Digital(Pedido):
    def __init__(self, client, status, payment,shipping):
        super.__init__("digital",client, status, payment,shipping)         
            
class FactoryPedidos():
    def crear_Pedido(self, client, status, payment, shipping, order_type):
        if "fisico"==order_type:
            return Fisico(client, status, payment,shipping)
        elif "digital"==order_type:
            return Digital(client, status, payment,shipping)
        else:
            return ValueError("")
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class PedidoService:
    def __init__(self):
        self.factory =FactoryPedidos()


    def listar(self):
        return {index: pedido.__dict__ for index, pedido in pedidos.items()}

class PedidoRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.pedido = PedidoService()
        super().__init__(*args, **kwargs)

   
    def do_GET(self):
        if self.path == "/orders":
            response_data = self.pedido.listar()
            HTTPDataHandler.handle_response(self, 200, response_data)
            
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"mensaje": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PedidoRequestHandler)
        print("Iniciando servidor web")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    main()