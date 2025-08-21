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

## ⚡ Quick Start

### 1. Install python (You can skip that part if already installed version >=3.12)
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
source .env
set +a
```

### 6. Start the server
```bash
python server.py
```

By default, the server is available at:  
👉 `http://localhost:8000`

### 7. Update project
1. Pull repository
    ```bash
    cd <repo-name>
    git pull
    ```
2. Repeat steps 3-6

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

Use following environment variables in `.env` file for configuration:

| Variable       | Description                     | Default | Comment                                                                                    |
|----------------|---------------------------------|---------|--------------------------------------------------------------------------------------------|
| `SERVER_IP`     | Server ip                       | `0.0.0.0` | Do not change if using docker. Otherwise - 0.0.0.0 will be only accessible from localhost. |
| `PORT`         | Server port                     | `8000`  | Use values >8000                                                                           |
| `LOGGING_LEVEL` | Logging level (`INFO`, `DEBUG`) | `INFO`  | Prefer to use 'INFO', case sensitive                                                       |

---

## 📩 Example Request

```bash
curl -X POST http://188.245.178.81:8183/hook \
  -H "Content-Type: application/json" \
  -H "Content-Encoding: gzip" \
  -H "x-hooktoken: test_hook_token" \
  -H "x-spreadbatchid: test_spead_batch_id" \
  -H "traceparent: 123" \
  -H "accept-encoding: gzip" \
  --data-binary @<(gzip -c <<'EOF'
{
    "ts": "1755778853375",
    "data": [
        {
            "profitIndexMax": 44.50681635926222,
            "profitIndexMin": 41.436818473380384,
            "profitIndexAvg": 42.823781352434395,
            "volume": 7841.103999999999,
            "buyPriceMin": 0.06235,
            "buyPriceMax": 0.06236,
            "buyPriceAvg": 0.062355249100126714,
            "sellPriceMin": 0.0882,
            "sellPriceMax": 0.0901,
            "sellPriceAvg": 0.08905812463653079,
            "exchangeBuy": "phemex",
            "exchangeSell": "huobi",
            "symbol": "ZKUSDT",
            "buyExchangeFundingProfitModifier": 0,
            "sellExchangeFundingProfitModifier": 0,
            "buyExchangeNextFundingTime": 0,
            "sellExchangeNextFundingTime": 0,
            "overallProfitIndexMax": 44.50681635926222,
            "overallProfitIndexMin": 41.436818473380384,
            "overallProfitIndexAvg": 42.823781352434395,
            "originalSymbol": "ZK-USDT|ZK-USDT",
            "volumeUsd": 593.62400523,
            "lifetime": 535105,
            "chainsBuy": [
                {
                    "chain": "zkeraeth",
                    "depositEnabled": true,
                    "withdrawEnabled": true,
                    "withdrawFee": 0.15264845
                }
            ],
            "chainsSell": [
                {
                    "chain": "zksync_era",
                    "depositEnabled": false,
                    "withdrawEnabled": false,
                    "withdrawFee": 1.2,
                    "minConfirm": 20
                }
            ],
            "updated": 0,
            "isFutures": false
        }
    ]
}
EOF
)
```

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
- [Support](mailto:support@your-company.com)  
