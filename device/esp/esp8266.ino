#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char *ssid = "galsiphone";      // replace with your actual SSID
const char *password = "12341234";    // replace with your actual password
const uint16_t port = 10319;
const char *host = "172.20.10.5";     // replace with your server IP

WiFiClient client;
bool connected = false;

unsigned long lastConnectionAttempt = 0;
const unsigned long connectionInterval = 5000; // 5 seconds

void setup() {
    delay(10000);  // Delay to ensure the serial monitor is ready
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
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi not connected!");
        delay(1000);
        return;
    }

    if (!connected) {
        if (millis() - lastConnectionAttempt >= connectionInterval) {
            lastConnectionAttempt = millis();
            Serial.println("Attempting to connect to server...");
            if (client.connect(host, port)) {
                Serial.println("Connected to server successfully!");
                connected = true;
            } else {
                Serial.println("Connection to host failed");
            }
        }
    } else {
        receiveCommands();
        sendKeystrokes();
    }

    // Other non-blocking tasks can be added here
}

void receiveCommands() {
    if (client.connected() && client.available()) {
        String command = client.readStringUntil('\n');
        command.trim();
        Serial.print("Received command: ");
        Serial.println(command);

        handleCommand(command);
    } else if (!client.connected()) {
        Serial.println("Disconnected from server");
        connected = false;
    }
}

void handleCommand(const String& command) {
    Serial.print("Handling command: ");
    Serial.println(command);

    if (command == "DO_SOMETHING") {
        // Execute specific action
    } else if (command == "DO_SOMETHING_ELSE") {
        // Execute another action
    }
}

void sendKeystrokes() {
    if (Serial.available()) {
        String keystrokes = Serial.readString();
        client.print(keystrokes);
        Serial.print("Sent to server: ");
        Serial.println(keystrokes);
    }
}
