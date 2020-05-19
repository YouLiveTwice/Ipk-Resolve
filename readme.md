# src.py

Src is a server writen in python which resolves dns questions and sends back answers to the clients. This server takes http request that can be either GET or POST. Both of these requests have to cointain a domain name or ip and type of resolution A or PTR. If the type is A then the server will resolve domain names to the ip adress. If the type PTR is used then the server will resolve ip address to the domain name.

## Run

To run this server use "make run" and give it a port number. The server will start on your current ip address and specified port number.

```bash
make run PORT=<>
```

## Usage
U can use the program curl to test the functionality ot this server.
GET request.
```python
curl ip address of server:specified port/resolve?name=ip or domain to resolve\&type=A or PTR

Example of GET request
curl localhost:5353/resolve?name=www.fit.vutbr.cz\&type=A
```
Post request will send a file which needs to have one request on each line
```python
curl --data-binary @file.txt -X POST http://ip address of server:specified port/dns-query

Esample of file.txt
www.fit.vutbr.cz:A
www.google.com:A
www.seznam.cz:A
147.229.14.131:PTR
ihned.cz:A

Example of POST request
curl --data-binary @queries.txt -X POST http://localhost:5353/dns-query
```