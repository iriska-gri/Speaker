# Архитектура



## Текущая (2024-08-09) конфигурация 

Сайт: dozvon


Архитектура состоит из следующих узлов
* Входной прокси
* Сервер приложений
* База данных

Входной прокси размещен на APP028

Сервер приложений и база данных - на APP040

```mermaid
graph LR;

subgraph CA
  User[Пользователь ЦА]
end

subgraph COD

  subgraph 028
    User-->|http://dozvon.cod2../|N[Nginx]
    User2[Наш пользователь]-->|http://dozvon/|N[Nginx]
  end

  subgraph  040
    N[Nginx]-->|10.252.44.60:9961/|APP
    APP --> BD[Postgress]
  end

end

```