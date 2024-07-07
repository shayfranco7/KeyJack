#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

const char* ssid = "Shays iphone";
const char* password = "shayfranco1";
const char* serverAddress = "our_server_ip_here";
const int serverPort = 10319;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to the TCP server
  if (!client.connect(serverAddress, serverPort)) {
    Serial.println("Connection to server failed");
    while(1);
  }
  Serial.println("Connected to server");
}

void loop() {
  if (!client.connected()) {
    Serial.println("Lost connection to server");
    reconnect();
  }

  // Check for incoming data from server
  while (client.available()) {
    String json = client.readStringUntil('\n');
    // Forward the received data to Arduino
    Serial.println(json);
  }

  // Check for data from Arduino to send to server
  if (Serial.available()) {
    String json = Serial.readStringUntil('\n');
    // Send the data to the server
    client.println(json);
  }
}

void reconnect() {
  // Try to reconnect
  Serial.println("Attempting to reconnect...");
  while (!client.connect(serverAddress, serverPort)) {
    Serial.println("Reconnection failed. Retrying in 5 seconds...");
    delay(5000);
  }
  Serial.println("Reconnected to server");
}
