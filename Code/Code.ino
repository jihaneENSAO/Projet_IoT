#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define DHTTYPE DHT11
#define DHTPIN 4   // GPIO4 sur ESP32

const char* ssid = "Adsl_inwi_07A9";
const char* password = "D842F70307A9";

const char* serverName = "http://192.168.1.3:8000/api/post/"; // Avant
//const char* serverName = "http://jihane04.pythonanywhere.com";

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  Serial.print("Humidity = ");
  Serial.print(humidity);
  Serial.print("% | Temperature = ");
  Serial.print(temperature);
  Serial.println(" °C");

  WiFiClient client;
  HTTPClient http;

  DynamicJsonDocument jsonDoc(200);
  jsonDoc["temp"] = temperature;
  jsonDoc["hum"] = humidity;

  String jsonStr;
  serializeJson(jsonDoc, jsonStr);

  http.begin(client, serverName);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(jsonStr);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
  delay(30000);
}
