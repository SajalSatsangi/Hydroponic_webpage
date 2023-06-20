#include <ArduinoJson.h>
#include <Wire.h>
#include <DHT.h>

int soilMoistureValue = 0;
int percentage = 0;
#define SENSOR_PIN A1
#define DHTTYPE DHT22
unsigned long delayTime;
uint8_t DHTPin = 2;
DHT dht(DHTPin, DHTTYPE);
float Temperature;
float Humidity;
float Temp_Fahrenheit;

void setup() {
  pinMode(3, OUTPUT);
  Serial.begin(9600);
  pinMode(DHTPin, INPUT);
}

void loop() {
  int sensorValue = analogRead(SENSOR_PIN);
  float nitrogen = map(sensorValue, 0, 1023, 0, 100);
  float phosphorus = map(sensorValue, 0, 1023, 0, 50);
  float potassium = map(sensorValue, 0, 1023, 0, 150);

  soilMoistureValue = analogRead(A0);

  Serial.println(percentage);

  percentage = map(soilMoistureValue, 490, 1023, 100, 0);

  if (percentage < 10) {
    Serial.println(" pump on");
    digitalWrite(3, LOW);
  }
  if (percentage > 80) {
    Serial.println("pump off");
    digitalWrite(3, HIGH);
  }

  Humidity = dht.readHumidity();
  Temperature = dht.readTemperature();
  Temp_Fahrenheit = dht.readTemperature(true);

  if (isnan(Humidity) || isnan(Temperature) || isnan(Temp_Fahrenheit)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(F("Humidity: "));
  Serial.print(Humidity);
  Serial.print(F("%  Temperature: "));
  Serial.print(Temperature);
  Serial.print(F("°C "));
  Serial.print(Temp_Fahrenheit);
  Serial.println(F("°F "));

  Serial.print("N:");
  Serial.print(nitrogen, 4);
  Serial.print("% ");
  Serial.print("P:");
  Serial.print(phosphorus, 4);
  Serial.print("% ");
  Serial.print("K:");
  Serial.print(potassium, 4);
  Serial.println("%");

  delay(5000);

  if (Serial.read() == 'j') {
    DynamicJsonDocument jsonBuffer(2048);
    JsonObject root = jsonBuffer.to<JsonObject>();

    if (percentage < 10) {
      root["Pump"] = "ON";
    }
    if (percentage > 80) {
      root["Pump"] = "OFF";
    }

    root["Humidity"] = Humidity;
    root["Temperature(celcius)"] = Temperature;
    root["Temperature(celcius)"] = Temp_Fahrenheit;
    root["N"] = nitrogen;
    root["P"] = phosphorus;
    root["K"] = potassium;

    serializeJson(root, Serial);
    Serial.println();
  }
}
