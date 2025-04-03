#ifndef SPEED_CONTROLLER_H
#define SPEED_CONTROLLER_H

#include <AccelStepper.h>
#include <Arduino.h>

// Pin definitions for Motor A
#define STEPPERA_DIR_PIN 32
#define STEPPERA_STEP_PIN 26

// Pin definitions for Motor B
#define STEPPERB_DIR_PIN 33
#define STEPPERB_STEP_PIN 27

// Pin definitions for Motor C
#define STEPPERC_DIR_PIN 25
#define STEPPERC_STEP_PIN 14

struct SpeedCart {
    float x, y, rot;
};

struct SpeedPolar {
    float r, angle, rot;
};

struct Motors {
    float A, B, C;
};

class SpeedController {
public:
    SpeedController();

    void begin();
    void run();
    void setSpeed(SpeedCart speed);
    void printWeelSpeed();
    void printRobotSpeed();
    void testWheels();
    SpeedCart convertPolarToCart(SpeedPolar polar);


private:
    const float steps_per_turns = 3200;
    const float rayon_robot = 0.13f;
    const float rayon_roue = 0.06f;
    const float motor_ratio =  steps_per_turns/(rayon_roue * 2 * PI); // pas/second
    const float max_speed = 10000000;
    const float acceleration = 100000;

    // Stepper motor instances
    AccelStepper stepperA{AccelStepper::DRIVER, STEPPERA_STEP_PIN, STEPPERA_DIR_PIN};
    AccelStepper stepperB{AccelStepper::DRIVER, STEPPERB_STEP_PIN, STEPPERB_DIR_PIN};
    AccelStepper stepperC{AccelStepper::DRIVER, STEPPERC_STEP_PIN, STEPPERC_DIR_PIN};

    Motors turns;
    SpeedCart speed;
};

SpeedCart convertPolarToCart(SpeedPolar polar);
SpeedPolar convertCartToPolar(SpeedCart cart);

#endif