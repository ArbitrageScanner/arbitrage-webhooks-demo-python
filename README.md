# 🚀 Demo Webhook Server for Arbitragescanner arbitrage-hooks API

Welcome to the official demo server for processing **webhook messages** from **Arbitragescanner arbitrage-hooks API**.  
This repository helps developers quickly understand how to integrate webhooks and handle events in their applications.

---

## 📖 Features

- Receive messages from webhooks  
- Log incoming requests  
- Basic processing and data storage  
- Easy to run with Docker or locally  

---

## 🔖 Before start

### 1. Fork repository
Click the **Fork** button at the top-right corner of this page to create your own copy of the repository.

### 1. Determine installation method
You can install and run this repository either manually, using [Quick start](#-quick-start) section, ot as a Docker container, using [Run with docker](#-run-with-docker) section.
If you are not confident in your abilities - use [Quick start](#-quick-start) section

### ⚠️ IMPORTANT
Ensure your server or local PC has static IP-address. If you have a dynamic IP-address - somewhere in close future your server would stop receiving requests from a webhook due to a `SERVER_IP` change

### 2. Establish your .env file
Create a file named `.env` and copy contents from [.env.example](.env.example) into `.env`

### 2. Customize config data
If you have decided to stick to [Quick start](#-quick-start):
1. Find your IP-address. For example - copy your IP-address from `IPv4` section on this [page](https://whatismyipaddress.com/)
2. Replace `SERVER_IP` variable value in newly created `.env` to copied value
3. If your port `8000` is occupied - chose other port between `8000` and `9000` and replace `SERVER_PORT` value with this. Otherwise - do not change nothing.

If you have decided to use [Run with docker](#-run-with-docker) section - do not change anything in .env

## ⚡ Quick Start

### 1. Install Python (Python 3.12 and above is recommended)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### 2. Clone the repository
```bash
git clone https://github.com/<your-org>/<repo-name>.git
cd <repo-name>
```

### 3. Create virtual environment
```bash
python3 -m venv .venv
```

### 5. Activate virtual environment
```bash
source .venv/bin/activate
```

### 6. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Set environmental variables reading from file
```bash
set -a
source .env
set +a
```

### 7. Start the server
```bash
python server.py
```

By default, the server is available at:  
👉 `http://localhost:8000`

### 7. Test your server
Send POST-request using this [Postman collection request](https://www.postman.com/arbscanner/workspace/arbscanner-b2b-api/request/23775304-894ae89e-a7f4-42c6-a3d1-144f5eadee68?action=share&source=copy-link&creator=23775304)
1. Open [request](https://www.postman.com/arbscanner/workspace/arbscanner-b2b-api/request/23775304-894ae89e-a7f4-42c6-a3d1-144f5eadee68?action=share&source=copy-link&creator=23775304)
2. Replace `ip_address` with your server IP-address
3. Replace `port` with your `SERVER_PORT` value from .env 
4. Replace `path` with desired endpoint path (defaults to `/hook`)
5. Press `Send`
6. Open `<SERVER_IP>:<SERVER_PORT>/stats/test_hook_token` in your browser
7. If request payload is parsed successfully - it will be shown in `/stats/test_hook_token` meaning everything works fine.
If not - read logs in `/app` folder
---

## 🐳 Run with Docker
### Installation
```bash
docker compose up --build -d
```
### Getting container name/id
```bash
docker ps
```
### Check container logs
```bash
docker logs webhooks_acceptor -f
```
- Logs can also be accessed directly from file in the `logs` folder. 
---

## 🛠 Configuration

Use following environment variables in [](.env.example) file for configuration:

| Variable       | Description                     | Default | Comment                        |
|----------------|---------------------------------|---------|--------------------------------|
| `SERVER_IP`     | Server ip                       | `0.0.0.0` | Do not change if using Docker. |
| `PORT`         | Server port                     | `8000`  | Use values >= 8000             |
| `LOGGING_LEVEL` | Logging level (`INFO`, `DEBUG`) | `INFO`  | Prefer to use 'INFO', case sensitive |

---

---

## 🏗 Project Structure
```
├── src/
│   ├── models.py        # pydantic models
│   └── server.py       # main server script
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing
We welcome your PRs, issues, and ideas!  

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/my-feature`)  
3. Submit a PR 🚀  

---

## 📜 License
This project is licensed under the **MIT License**.  
See [LICENSE](./LICENSE) for details.

---

## 🌐 Useful Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [What is a webhook and how to use it?](https://www.geeksforgeeks.org/blogs/what-is-a-webhook-and-how-to-use-it/)
- [What is Docker?](https://docs.docker.com/get-started/docker-overview/)
- [Our Website](https://arbitragescanner.io/)  
- [Support](https://t.me/arbitrage_scanner_support_bot)  
