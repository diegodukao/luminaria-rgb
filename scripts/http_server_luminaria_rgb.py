#!/usr/bin/env python2

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def http_response(self, content, answer=200):
        self.send_response(answer)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        modes = ['modo-intimo', 'dance', 'aleatorio']
        ip, port = self.client_address
        resource = self.path.split('?')[0][1:]
        if resource.startswith('LED-') or resource in modes:
            self.server.arduino.write(resource + '\n')
            self.server.arduino.flush()
            result = self.server.arduino.readline()
            self.http_response(result)
        else:
            self.http_response('This URL does not exist!', 404)


if __name__ == "__main__":
    import glob
    import serial

    try:
        BAUD_RATE = 9600
        TIMEOUT = 0.1
        server = HTTPServer(('', 80), Handler)
        serial_ports = glob.glob('/dev/ttyUSB0') + glob.glob('/dev/ttyACM0')
        if not len(serial_ports):
            print 'ERROR: no Arduino found'
            exit(1)
        serial_port = serial_ports[0]
        server.arduino = serial.Serial(serial_port, BAUD_RATE, timeout=TIMEOUT)
        server.arduino.write('LED-000000')
        server.arduino.flush()
        server.arduino.read()
        print("HAI")
        print("CAN HAS PORT 80?")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKTHXBYE")
        server.shutdown()
        server.socket.close()
