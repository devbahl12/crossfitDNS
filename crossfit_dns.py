import asyncio
import time
import subprocess
import platform
import argparse
from dnslib import RR, A, QTYPE
from dnslib.server import DNSServer, BaseResolver

DOMAIN = "snl-columbia-university.github.io"
SERVERS = ["34.171.194.225", "34.174.196.10"]
PING_INTERVAL = 10
TTL = 10

latencies = {ip: float("inf") for ip in SERVERS}
best_server = SERVERS[0]

def get_ping_cmd(ip):
    system = platform.system().lower()
    if system == "darwin":
        return ["ping", "-c", "1", "-W", "1000", ip]
    elif system == "linux":
        return ["ping", "-c", "1", "-W", "1", ip]
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

async def ping_loop():
    global best_server
    while True:
        for ip in SERVERS:
            try:
                result = subprocess.run(get_ping_cmd(ip), capture_output=True, text=True)
                if "time=" in result.stdout:
                    latency = float(result.stdout.split("time=")[1].split(" ")[0])
                    latencies[ip] = latency
                    print(f"[{time.ctime()}] Ping {ip}: {latency:.2f} ms")
                else:
                    latencies[ip] = float("inf")
                    print(f"[{time.ctime()}] Ping {ip} failed")
            except Exception as e:
                latencies[ip] = float("inf")
                print(f"[{time.ctime()}] Error pinging {ip}: {e}")
        best_server = min(latencies, key=latencies.get)
        print(f"[{time.ctime()}] Current best server: {best_server}")
        await asyncio.sleep(PING_INTERVAL)

class Resolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname).rstrip(".")
        qtype = QTYPE[request.q.qtype]
        print(f"[DNS Query] From {handler.client_address[0]} asking for {qname} ({qtype})")
        if qname == DOMAIN and qtype in ("A", "ANY"):
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(best_server), ttl=TTL))
            print(f"[DNS Response] Returned {best_server} for {qname}")
            return reply
        else:
            return request.reply()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CROSSFIT DNS Server")
    parser.add_argument("--port", type=int, default=53, help="Port to run the DNS server on")
    args = parser.parse_args()

    resolver = Resolver()
    server = DNSServer(resolver, port=args.port, address="0.0.0.0")
    server.start_thread()
    print(f"CROSSFIT DNS server starting on UDP/{args.port}...")
    try:
        asyncio.run(ping_loop())
    except KeyboardInterrupt:
        print("Shutting down...")