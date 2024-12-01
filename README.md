# Crypto Arbitrage between CEX and DEX

This project focuses on crypto arbitrage between centralized exchanges (CEX) and decentralized exchanges (DEX). The entire codebase is implemented in **Python** and utilizes several key modules: **Redis**, **Web3**, and **CCXT**.

In this project, **Redis** serves as the database. By storing all data in memory, Redis significantly speeds up the processes of data storage and retrieval, which is crucial for an effective arbitrage program. This setup enhances performance and responsiveness, enabling timely trading decisions.

## Main modules used in python
|Modules | Function|Figure|
-------|--------|----|
ccxt | API of CEX| ![ccxt](https://github.com/ccxt.png?size=40)
web3.py| Connect with DEX| ![web3](https://avatars.githubusercontent.com/u/6250754?s=48&v=4)
redis| Control Database Redis| ![redis](https://github.com/redis.png?size=40)
------

**Program v2.0** leverages the WebSocket method to fetch data from centralized exchanges (CEX). This approach minimizes latency, significantly speeding up the data retrieval process. By using WebSockets, the program can receive real-time updates, ensuring more timely and efficient trading decisions.