# SwiftEdge CDN 🚀

SwiftEdge is a multi-threaded edge caching server that simulates core CDN (Content Delivery Network) behavior.

This project demonstrates caching, TTL-based expiration, load balancing, and concurrent request handling — inspired by real-world CDN architectures like Akamai.

---

## 📌 Features

- ✅ Multi-threaded client handling
- ✅ TTL-based disk caching
- ✅ Cache HIT / MISS detection
- ✅ Cache expiration logic
- ✅ Origin server fetching
- ✅ Basic load balancing simulation
- ✅ Structured logging support

---

## 🏗 Architecture Overview

Client → Edge Server → Origin Server  
          ↳ Cache (Disk-based)

- If content exists in cache and is valid → serve immediately
- If expired or missing → fetch from origin → update cache → serve client

---

## ⚙️ Technologies Used

- Python (Socket Programming)
- Threading
- File System Caching
- Basic Load Balancing Logic

---

## 🚀 How To Run

### 1️⃣ Start Origin Server

```
mkdir origin
cd origin
echo "Hello from Origin Server" > index.html
python3 -m http.server 8001
```

### 2️⃣ Run Edge Server

```
python3 edge_server.py
```

### 3️⃣ Send Request

```
curl localhost:8080
```

---

## 🧠 Concepts Implemented

- Time-to-Live (TTL)
- Cache Expiration
- Concurrent Request Handling
- Basic Load Distribution
- Edge-to-Origin Communication

---

## 🎯 Future Improvements

- In-memory LRU cache
- Cache size-based eviction
- Reverse proxy implementation
- Kubernetes deployment
- Performance benchmarking

---

## 📚 Why This Project?

This project was built to understand real-world CDN behavior and distributed edge architectures similar to production systems.

---

## 👨‍💻 Author

Akash Manikanta
