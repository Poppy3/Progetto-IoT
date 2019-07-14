#include <dht_nonblocking.h>

#define DHT_SENSOR_TYPE DHT_TYPE_11

static const int lightPin1 = A0;
static const int lightPin2 = A1;
static const int thermoPin = A2;
static const int dhtDataPin = 2;

static const unsigned long DELAY_TIME = 2500;

DHT_nonblocking dht_sensor(dhtDataPin, DHT_SENSOR_TYPE);


void setup() {
  Serial.begin(9600);
}


bool measure_dht_with_delay(float *temperature, float *humidity)
{
  static unsigned long delayStart = millis();
  if(millis() - delayStart >= DELAY_TIME)
  {
    if(dht_sensor.measure(temperature, humidity) == true)
    {
      delayStart = millis();
      return(true);
    }
  }
  return(false);
}


bool measure_thermometer(float *tempC)
{
  int tempReading = analogRead(thermoPin);
  // Temp Kelvin
  double tempK = log(10000.0 * ((1024.0 / tempReading - 1)));
  tempK = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * tempK * tempK)) * tempK); 
  *tempC = tempK - 273.15;  // Convert Kelvin to Celcius
  return(true);
}


bool measure_photocell1(int *light)
{
  *light = analogRead(lightPin1);
  return(true);
}

bool measure_photocell2(int *light)
{
  *light = analogRead(lightPin2);
  return(true);
}


void loop() {
  float dht_temperature;
  float dht_humidity;
  float thermometer_temperature;
  int photocell_light1;
  int photocell_light2;
  
  if(measure_dht_with_delay(&dht_temperature, &dht_humidity) == true)
  {
    Serial.print("[DHT11]       T = ");
    Serial.print(dht_temperature, 2);
    Serial.print(" deg. C, H = ");
    Serial.print(dht_humidity, 2);
    Serial.println("%");

    measure_thermometer(&thermometer_temperature);
    Serial.print("[THERMISTOR]  T = ");
    Serial.print(thermometer_temperature, 2);
    Serial.println(" deg. C");

    measure_photocell1(&photocell_light1);
    measure_photocell2(&photocell_light2);
    Serial.print("[PHOTOCELL-1] L = ");
    Serial.println(photocell_light1);
    Serial.print("[PHOTOCELL-2] L = ");
    Serial.println(photocell_light2);
    Serial.println("------");
  }

}
