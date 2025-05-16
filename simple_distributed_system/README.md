# Простая распределенная система


Перед запуском сервисов необходимо сгенерировать сертификат для работы HTTPS  

[Инструкция по генерации сертификата для linux/macos](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/securing_networks/creating-and-managing-tls-keys-and-certificates_securing-networks#creating-a-private-ca-using-openssl_creating-and-managing-tls-keys-and-certificates)

Запуск сервисов:  
```sh
docker compose up -d
```

После запуска сервисы должны быть доступны по протоколу https.  

Порт 5000 - сервис авторизации  
Порт 5001 - сервис заказов  


Для сервисов доступен swagger по эндпоинту **/docs**
