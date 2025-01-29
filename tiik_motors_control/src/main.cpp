#include <Arduino.h>
#include <SpeedController.h>
#include <Wire.h>

#define I2C_SLAVE_ADDRESS 0x08
#define BUFFER_SIZE 32

void receiveEvent(int);
SpeedCart convertStringToSpeedCart(const char input[]);
void square();

SpeedController tiik;

unsigned long pre_time = 0;
int state = 0;

// Define speed vectors for square path
float SPEED_VALUE = 0.5f;

SpeedCart speed[] = {
    {SPEED_VALUE, 0.0, 0.0},  // Move right
    {0.0, SPEED_VALUE, 0.0},  // Move forward
    {-SPEED_VALUE, 0.0, 0.0}, // Move left
    {0.0, -SPEED_VALUE, 0.0}  // Move backward
};

unsigned long side_duration;

void setup() {
    tiik.begin();
    // Serial.begin(115200);
  
    // Initialize the I2C slave
    Wire.begin(I2C_SLAVE_ADDRESS);
    Wire.onReceive(receiveEvent);
    // Serial.println("ESP32 I2C Slave initialized.");
}

void loop() {
    tiik.run();
}

void square(){
    static long pre_time = millis();
    static long state = 0;
    if (millis() - pre_time > 1000){
        tiik.setSpeed(speed[state]);
        state ++;
        state = state % 4;
        pre_time = millis();
    }
}

void receiveEvent(int bytesReceived) {
    char buffer[BUFFER_SIZE];
    int i = 0;
    
    // Serial.print("Bytes available: ");
    // Serial.println(Wire.available());

    if (Wire.available() > 0) {
        Wire.read();
    }

    while (Wire.available() > 0 && i < BUFFER_SIZE - 1) {
        char receivedByte = Wire.read();
        buffer[i++] = receivedByte;
    }
    

    buffer[i] = '\0';
    

    // Serial.print("Received: ");
    // Serial.println(buffer);

    SpeedCart speed = convertStringToSpeedCart(buffer);
    tiik.setSpeed(speed);
}

SpeedCart convertStringToSpeedCart(const char input[]) {
    SpeedCart speed;
    sscanf(input, "x: %f, y: %f, r: %f", &speed.x, &speed.y, &speed.rot);
    return speed;
}