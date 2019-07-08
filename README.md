# Progetto IoT - Garduino (kind of)

L'idea per ora è usare un arduino per leggere i valori dai sensori. La comunicazione con raspberry (o pc) potrebbe essere gestita con seriale, o wifi/bluetooth(ma richiede componenti aggiuntivi).
Per l'interfaccia pensavamo a telegram, come una chat di comunicazione con la tua pianta.

#### Risorse

-- Tutorial su bot telegram
https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/?utm_source=medium&utm_medium=chatbotslife.com&utm_campaign=telegrambotwithpython&utm_content=continuereading


#### Codice giardinino

https://github.com/gradyh/GradyHillhouseGarduino.git


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
