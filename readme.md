# CROSSFIT Exploratory Project – Latency-Aware DNS Server  

## 📌 Overview  
This project is part of the **CROSSFIT (Content-aware Routing Over Standard Service For Interactive Technologies)** initiative.  
The goal is to demonstrate a simplified **authoritative DNS server** that dynamically steers traffic for XR applications based on latency measurements.  

Traditional DNS and BGP cannot adapt to real-time performance changes. Our prototype DNS server:  
- Periodically measures latency to two backend servers.  
- Selects the lowest-latency server dynamically.  
- Answers DNS queries for `snl-columbia-university.github.io` with that server’s IP.  
- Logs all measurements, queries, and responses.  

---

## ⚙️ Features  
- Active latency measurement every **10 seconds**  
- Returns best server IP dynamically  
- Configurable DNS port via `--port` flag  
- Logs include:  
  - Ping results  
  - Incoming queries  
  - Outgoing responses  

---

## 🖥️ Requirements  
- Python 3.8+  
- [`dnslib`](https://pypi.org/project/dnslib/) library  

Install dependencies:  
```bash
pip install dnslib

## 🚀 How to Run  

## Run on standard DNS port (requires root/sudo):  
```bash
sudo python3 crossfit_dns.py --port 53

## Run on custom port (no root needed, e.g., 8053):

python3 crossfit_dns.py --port 8053

## 🔧 How to Test  

## If running on port 53:

dig @127.0.0.1 snl-columbia-university.github.io

## If running on custom port (e.g., 8053):

dig @127.0.0.1 -p 5353 snl-columbia-university.github.io

## Example Logs

![alt text](/logs.png)

## Test Result

![alt text](/testss.png)