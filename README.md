# 🚀 Demo Webhook Server for [Your API Name]

Welcome to the official demo server for processing **webhook messages** from [Your API Name].  
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
Ensure your server or local PC has static IP-address, otherwise webhook requests would not be able to reach your app.

### 2. Establish your .env file
Create a file named `.env` and copy contents from [.env.example](.env.example) into `.env`

### 2. Customize config data
If you have decided to stick to [Quick start](#-quick-start):
1. Find your IP-address. For example - copy your IP-address from `IPv4` section on this [page](https://whatismyipaddress.com/)
2. Replace `SERVER_IP` variable value in newly created `.env` to copied value
3. If your port `8000` is occupied - chose other port between `8000` and `9000` and replace `SERVER_PORT` value with this. Otherwise - do not change nothing.

If you have decided to use [Run with docker](#-run-with-docker) section - do not change anything in .env

## ⚡ Quick Start

### 1. Install Python (You can skip that part if you already have an installed Python instance with version >=3.12)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### 2. Clone the repository
```bash
git clone https://github.com/<your-org>/<repo-name>.git
cd <repo-name>
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
```

### 3. Activate virtual environment
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set environmental variables reading from file
```bash
set -a
source .env.example
set +a
```

### 6. Start the server
```bash
python server.py
```

By default, the server is available at:  
👉 `http://localhost:8000`

### 7. Test your server
Send POST-request using this [collection](postman link)
1. Open collection
2. Select `<endpoint name>`
3. Replace `<server_host>` by your values using following format: `<SERVER_IP>:<SERVER_PORT>`
4. Press `Send`
5. Open `<SERVER_IP>:<SERVER_PORT>/stats` in your browser
6. If request payload is parsed successfully - it will be shown in `/stats` meaning everything works fine.
7. If not - read logs in `/app` folder
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
