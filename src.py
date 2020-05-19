import sys
import socket 
from urllib.parse import urlparse

try:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    try:
        port = int(sys.argv[1])   
    except:
        print ("This program needs a PORT= 1 to 65535")
        sys.exit(1)

    if not (port in range(1, 65535)):
        print ("This program needs a PORT= 1 to 65535")
        sys.exit(1)

    def dns(dns_type, domein):
        addr = ""
        returnCode = ""
        if dns_type == 'A':
            #TODO musim oravit prijima i ip
            if domein.find(".") != -1 and test_ip(domein) == -1:
                try:
                    addr = socket.gethostbyname(domein)
                    returnCode = "200"
                except:
                    addr = "Domain name was not found"
                    returnCode = "404"
            else:
                returnCode = "400"
                addr = "Type=A needs a valid domain name and this domain name is not valid"
        elif dns_type == 'PTR':
            if test_ip(domein) != -1: 
                try:
                    addr = socket.gethostbyaddr(domein)[0]
                    returnCode = "200"
                except:
                    addr = "IP address was not found"
                    returnCode = "404"
            else:
                returnCode = "400"
                addr = "Type=PTR needs a valid IP address and this IP address is not valid"
        else:
            addr = "Bad request"
            returnCode = "400"
        return [addr, returnCode]

    def test_ip(ip):
        try:
            ip = ip.split('.')
            if len(ip) == 4:
                for sub in ip:
                    if not(int(sub) in range(0, 255)):
                        return -1
                return 0
            else:
                return -1
        except:
            return -1
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(5)
        dir(sock)
        print("This server is running on ip=" + ip + " and port=" + str(port))
    except:
        print("This port is curentlly occupied, please close the application on this port or try a different port")
        sys.exit(1)

    while 1:
        clientsocket, address = sock.accept()
        data = clientsocket.recv(1024)
        data = data.decode("utf-8")
        if data.find('GET') != -1:
            try:
                tmp_string = data.split("name=")[1]
                domein = tmp_string.split("&")[0]
                domein = urlparse(domein).path
                tmp_string = tmp_string.split("type=")[1]
                dns_type = tmp_string.split(' ')[0]
                result, returnCode = dns(dns_type, domein)
                if returnCode != "200":
                    answer = result + "\n"
                else:
                    answer = domein + ':' + dns_type + '=' + result + "\n"
            except:
                returnCode = "400"
                answer = "Bad request\n"

        elif data.find('POST') != -1:
            try:
                returnCode = "200"
                data = data.split("\n\r")[1]
                data = data.replace(" ", "")
                data = data.replace("\t", "")
                data = data.strip()
                array_request = data.split("\n")
                answer = ''
                for request in array_request:
                    domein, dns_type = request.split(':')
                    domein = urlparse(domein).path
                    result, returnCode  = dns(dns_type, domein)
                    if returnCode != "200":
                        result = ""
                    answer = answer + domein + ':' + dns_type + '=' + result + "\n"
                    if returnCode == "400":
                        answer = "Bad request\n"
            except:
                returnCode = "400"
                answer = "Bad request\n"

        else:
            answer = "This server does not support this request\n"
            returnCode = "405"
    
        if returnCode == "200":
            returnStatement = " OK"

        else:
            returnStatement = " WARNING"
        return_http = "HTTP/1.1 " + returnCode + returnStatement + "\n\n" + answer
        return_http = return_http.encode("utf-8")
        clientsocket.sendall(return_http)
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()

except(KeyboardInterrupt):
    try:
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()
    except:
        pass
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print("\nClosing the server. Have a nice day")
    sys.exit()
