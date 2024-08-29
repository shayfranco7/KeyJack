#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include "math.h"
const char *ssid = "CSBOT";
const char *password = "";
const uint16_t port = 10319;
const char *host = "10.10.245.147";

WiFiClient client;
bool connected = false;
unsigned long lastConnectionAttempt = 0;
const unsigned long connectionInterval = 5000; // 5 seconds
int rema=0;

void setup() {
    delay(10000);  // Delay to ensure the serial monitor is ready
    Serial.begin(115200);
    Serial.println();
   // Serial.println("Connecting to WiFi...");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 20) {
        delay(500);
        Serial.print(".");
        retries++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
       // Serial.print("Connected to WiFi. IP address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println();
       // Serial.println("Failed to connect to WiFi.");
    }
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
       // Serial.println("WiFi not connected!");
        delay(1000);
        return;
    }
    if (!connected) {
        if (millis() - lastConnectionAttempt >= connectionInterval) {
            lastConnectionAttempt = millis();
           // Serial.println("Attempting to connect to server...");
            if (client.connect(host, port)) {
            //    Serial.println("Connected to server successfully!");
                connected = true;
            } else {
             //   Serial.println("Connection to host failed");
            }
        }
    } else {
        receiveCommands();
        sendKeystrokes();
        sendDataToArduino(); // New function to send data to Arduino
    }
    // Other non-blocking tasks can be added here
}
void sendCommandSerial(String command){
  Serial.println(command);
  // int d = min((int) (max(200,(int) (8*command.length()+50))),2000);
  int d = max(400,(int) (8*command.length()+50));
  if(command.startsWith("ENTER"))
    delay(500);
  else
    delay(min(2000,rema + d));
  if(d>2000)
    rema=d-2000;
  else
    rema=0;
  //Serial.println(d+rema);
}
void receiveCommands() {
    if (client.connected() && client.available()) {
        String command = client.readStringUntil('\n');
        command.trim();
        sendCommandSerial(command);
        //Serial.print(command);
        // String cmd = "";
        // for(int i = 0; i<command.length(); i++){
        //   cmd = "";
        //   while(command.charAt(i) != '\n'){
        //     cmd += command.charAt(i);
        //     i++;
        //   }
        //     Serial.println(cmd);
        //     delay(2000);

        //}
    } else if (!client.connected()) {
        Serial.println("Disconnected from server");
        connected = false;
    }
}
void sendKeystrokes() {
    if (Serial.available()) {
        String keystrokes = Serial.readString();
        client.print(keystrokes);
    }
}

void sendDataToArduino() {
    static unsigned long lastSendTime = 0;
    const unsigned long sendInterval = 1000; // Send every 1 second

    if (millis() - lastSendTime >= sendInterval) {
        lastSendTime = millis();
        
        // Example data to send
        String dataToSend = "Data from NodeMCU";
        
        // Send data to Arduino
    }
}
