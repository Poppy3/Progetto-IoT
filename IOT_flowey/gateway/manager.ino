#include <dht_nonblocking.h>

#define DHT_SENSOR_TYPE DHT_TYPE_11

static const int thermoPin = A0;
static const int lightPin1 = A1;
static const int lightPin2 = A2;
static const int dhtDataPin = 2;
static const int hygroDataPin1 = A3;
static const int hygroDataPin2 = A4;
static const int hygroDataPin3 = A5;

static const int ledRPin = 11;
static const int ledGPin = 10;
static const int ledBPin = 9;

static const unsigned long DELAY_TIME = 600000; // 10 minutes in milliseconds

static const String device_id = "ARDUINO001";

DHT_nonblocking dht_sensor(dhtDataPin, DHT_SENSOR_TYPE);

int ledR = 0;
int ledG = 255;
int ledB = 0;


void setup() {
  pinMode(ledRPin, OUTPUT);
  pinMode(ledGPin, OUTPUT);
  pinMode(ledBPin, OUTPUT);
  Serial.begin(9600);
}


void measure_hygrometer(int *humidity, int pin)
{
  *humidity = analogRead(pin);
}


bool measure_dht_with_delay(float *temperature, float *humidity)
{
  static unsigned long delayStart = millis();
  if (millis() - delayStart >= DELAY_TIME)
  {
    if (dht_sensor.measure(temperature, humidity) == true)
    {
      delayStart = millis();
      return (true);
    }
  }
  return (false);
}


int read_serial()
{
  int incomingByte = -1;
  if (Serial.available() > 0){
    incomingByte = Serial.read();
  }
  return(incomingByte);
}


void measure_thermometer(float *tempC)
{
  int tempReading = analogRead(thermoPin);
  // Temp Kelvin
  double tempK = log(10000.0 * ((1024.0 / tempReading - 1)));
  tempK = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * tempK * tempK)) * tempK);
  *tempC = tempK - 273.15;  // Convert Kelvin to Celcius
}


void measure_photocell(int *light, int pin)
{
  *light = analogRead(pin);
}


void color_led(int r, int g, int b)
{
  analogWrite(ledRPin, r);
  analogWrite(ledGPin, g);
  analogWrite(ledBPin, b);
}

void manage_led()
{
  int serial_value = read_serial();
  switch (serial_value) {
    case '0': // green light
      ledR = 0;   ledG = 200; ledB = 0;
      break;
    case '1': // yellow light
      ledR = 255; ledG = 200; ledB = 0;
      break;
    case '2': // orange light
      ledR = 255; ledG = 40; ledB = 0;
      break;
    case '3': // red light
      ledR = 255; ledG = 0;   ledB = 0;
      break;
    default: // nothing
      break;
  }
  color_led(ledR, ledG, ledB);
}


void print_values_as_json(float dht_t, float dht_h,
                          float t,
                          int l1, int l2,
                          int h1, int h2, int h3)
{
  Serial.print("{");
  Serial.print("\"device_id\":\"");     Serial.print(device_id); Serial.print("\",");
  Serial.print("\"timestamp\":");       Serial.print(millis());  Serial.print(",");
  Serial.print("\"dht_temperature\":"); Serial.print(dht_t);     Serial.print(",");
  Serial.print("\"dht_humidity\":");    Serial.print(dht_h);     Serial.print(",");
  Serial.print("\"temperature\":");     Serial.print(t);         Serial.print(",");
  Serial.print("\"luminosity_1\":");    Serial.print(l1);        Serial.print(",");
  Serial.print("\"luminosity_2\":");    Serial.print(l2);        Serial.print(",");
  Serial.print("\"humidity_1\":");      Serial.print(h1);        Serial.print(",");
  Serial.print("\"humidity_2\":");      Serial.print(h2);        Serial.print(",");
  Serial.print("\"humidity_3\":");      Serial.print(h3);
  Serial.println("}");
}


void loop() {
  float dht_temperature = 0;
  float dht_humidity = 0;
  float thermometer_temperature = 0;
  int photocell_light1 = 0;
  int photocell_light2 = 0;
  int hygrometer_humidity1 = 0;
  int hygrometer_humidity2 = 0;
  int hygrometer_humidity3 = 0;

  /*** manage measurements ***/
  if (measure_dht_with_delay(&dht_temperature, &dht_humidity) == true)
  {
    measure_thermometer(&thermometer_temperature);

    measure_photocell(&photocell_light1, lightPin1);
    measure_photocell(&photocell_light2, lightPin2);

    measure_hygrometer(&hygrometer_humidity1, hygroDataPin1);
    measure_hygrometer(&hygrometer_humidity2, hygroDataPin2);
    measure_hygrometer(&hygrometer_humidity3, hygroDataPin3);

    print_values_as_json(dht_temperature, dht_humidity,
                         thermometer_temperature,
                         photocell_light1, photocell_light2,
                         hygrometer_humidity1, hygrometer_humidity2, hygrometer_humidity3);
  }

  /*** manage rgb led ***/
  manage_led();
  
}
