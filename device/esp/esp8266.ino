#include <ESP8266WiFi.h>
#include <WiFiClient.h>

#define BAUD_RATE 115200

/* ============= CHANGE WIFI CREDENTIALS ============= */
const char *ssid = "";       // replace with your actual SSID
const char *password = ""; // replace with your actual password
/* ============= ======================= ============= */

const uint16_t port = 10319;
const char *host = "172.20.10.5"; // replace with your server IP
WiFiClient client;
bool connected = false;

void setup() {
    Serial.begin(BAUD_RATE);
    delay(100); // Give some time for the serial to initialize
    Serial.println();
    Serial.println("Connecting to WiFi...");
    
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password); // change it to your ssid and password
    
    // Attempt to connect to WiFi network
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
        client.println("Hello From ESP8266");
        delay(250);
        while (client.available() > 0) {
            char c = client.read();
            Serial.write(c);
        }
        Serial.println();
        client.stop();
        connected = true; // Set the flag to true to indicate a successful connection
    } else {
        // Optional: You can add code here to periodically check the connection or handle other tasks
        delay(5000); // Example delay
    }
}
