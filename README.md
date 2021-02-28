# Progetto IoT - Garduino (kind of)

L'idea per ora è usare un arduino per leggere i valori dai sensori. La comunicazione con raspberry (o pc) potrebbe essere gestita con seriale, o wifi/bluetooth(ma richiede componenti aggiuntivi).
Per l'interfaccia pensavamo a telegram, come una chat di comunicazione con la tua pianta.

#### Note e Roadmap

https://docs.google.com/document/d/1bADpilcZcmvr3uMJ3wHkrVnHlY_TWHJ9U9sN4OMp0S4/edit?usp=sharing

#### Risorse

-- Tutorial su bot telegram
https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/?utm_source=medium&utm_medium=chatbotslife.com&utm_campaign=telegrambotwithpython&utm_content=continuereading


#### Codice giardinino

https://github.com/gradyh/GradyHillhouseGarduino.git

#### Progetto pazzesco
https://create.arduino.cc/projecthub/dymonxd/grow-it-yourself-giy-bec993?ref=tag&ref_id=garden&offset=2

#### Token Ngrok di Asia
3ZHQNQ77QjY9tm273GSnB_5cZzYeXghN4HyG7R9w1r6

#### Token Bot Flowey
744755426:AAHCNYYTctEwvwW_PBzBK7NV8fh1pHkqaiQ

#### Tesina
https://docs.google.com/document/d/1NNB9fvqPyqg2SD_VwvQb1ESI88l5bCgdshtuKrfREr8/edit?usp=sharing

##### esempio richiesta post a ngrok (al posto del webhook)
{
  "update_id": 671372324,
  "message": {
    "message_id": 40,
    "from": {
      "id": 820844162,
      "is_bot": false,
      "first_name": "Asia",
      "last_name": "Bergamini",
      "language_code": "it"
    },
    "chat": {
      "id": 353051365,
      "first_name": "Asia",
      "last_name": "Bergamini",
      "type": "private"
    },
    "date": 1562599569,
    "text": "TESTO DEL MESSAGGIO"
  }
}


#### Passaggi per rimettere su il bot di Telegram

https://api.telegram.org/bot744755426:AAHCNYYTctEwvwW_PBzBK7NV8fh1pHkqaiQ/getUpdates
Giusto se serve vedere l'ultimo messaggio ricevuto (non finziona se un webhook è attivo)

1 - far partire Ngrok
./ngrok http 8080

2 - Aggironare il webhook
https://api.telegram.org/bot744755426:AAHCNYYTctEwvwW_PBzBK7NV8fh1pHkqaiQ/getWebhookInfo
---> https://api.telegram.org/bot744755426:AAHCNYYTctEwvwW_PBzBK7NV8fh1pHkqaiQ/setWebHook?url=[nuovo ngrok url]  se necessita di essere aggiornato. Oppure setWebHook può essere chiamato senza url per cancellare il webhook.

Nota: telegram vuole solo webhook https, non usare solo http.

