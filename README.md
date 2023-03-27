# Peon-tgbot

PeonBot 是 SaweiBot 的原型專案，透過累計點數機制管理群組會員權限的 Telegram 機器人。 能夠將發言數未到達一定數量的會員限制使用貼圖、圖片、超連結等權限避免進群就受到噁圖攻擊、未成年色圖炸群等危害。

## Requipment

- Postgres (透過 Tortoise-orm 進行連接)。
- Reids (用於快取使用者資訊及群組設置)

note: 可自行更換為 mysql 、mariadb 等其他 Tortoise-orm 支援的關聯式資料庫。

## 使用案例

https://tassis.github.io/chats/-1001470287738/deletedmsg


