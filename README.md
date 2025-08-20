# Public webhook acceptor server

## Before start

This repo is made to be used as a docker container, but you can start it directly, by starting `server.py` from your .venv or using some packet manager, for example `pm2`
Config file for `pm2` is also included in the repo. 

## Preparations

Before start - specify SERVER_PORT in .env. You can use safely use 8080-8085 values. More on that:


## Installation

- Locate the target path, where repo will be cloned
e.g. cloning repo from ~/ or root/ wiil lead to creation of ~/public_webhooks_server_acceptor_python or root/public_webhooks_server_acceptor_python

- Perform following commands:

    ```
    cd public_webhooks_server_acceptor_python
    docker compose up --build -d
    ```

    > In case your server does not support modern docker syntax, you can upgrade your Docker on your own risk using following commands:
    > 
    >`No commands here yet`


After performing docker compose command the container should already be up and running.

You can check that by typing: 

`docker ps`

If everything is correct - in response to that command you will see the following (container id would be different, but other things would be the same):

|CONTAINER ID|IMAGE|COMMAND|CREATED|STATUS|PORTS|NAMES|
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
|fb7fe016d840|public_webhooks_server_acceptor_python-webhooks_acceptor|"sh -c 'uvicorn serv…"|7 minutes ago|Up 7 minutes|0.0.0.0:8183->8183/tcp, [::]:8183->8183/tcp|webhooks_acceptor|


## Usage

After that you can create your hooks by passing `http://{YOUR SERVER STATIC IP}:{SERVER PORT FROM .env}/hook` as your hook address and start receiving spread batches.

You can always access it via `http://{YOUR SERVER STATIC IP}:{SERVER PORT FROM .env}/stats` to see all hooks, that were received during current server session (meaning server is online) or http://{YOUR SERVER STATIC IP}:{SERVER PORT FROM .env}/stats/{hook_token} to get single hook data. 

You can get your hook hook_token either from /stats or from https://b2b.api.arbitragescanner.io/api/screener/v1/live/manage-hooks/list-hooks  (you have to pass your api key to get data from this endpoint.)

By default only last 10 spread batches are saved in order from newest to oldest. This is made in purpose of saving your server RAM, because saving data from multiple hooks, if old data is not deleted, would eat your RAM quite quickly.

You can specify hooks saving behaviour by changing number of saved hooks directly in code (simply commenting or deleting few lines of code, if you want to save all gathered data, look up for a comment lines in at the end of the accept_hook method) or create your own behaviour. For example, you can save hooks in file or create an endpoint, passing a request to would trigger data saving in file.

## Useful links
No links yet