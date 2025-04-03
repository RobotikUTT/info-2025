#include "SpeedController.h"

SpeedController::SpeedController(){

}

void SpeedController::begin()
{

    stepperA.setMaxSpeed(max_speed);  // Set the max speed (increase as needed)
    stepperB.setMaxSpeed(max_speed);  // Set the max speed (increase as needed)
    stepperC.setMaxSpeed(max_speed);  // Set the max speed (increase as needed)

    // Increase acceleration
    stepperA.setAcceleration(acceleration);  // Set the acceleration (increase as needed)
    stepperB.setAcceleration(acceleration);  // Set the acceleration (increase as needed)
    stepperC.setAcceleration(acceleration);  // Set the acceleration (increase as needed)
}

void SpeedController::setSpeed(SpeedCart speed) {
    this->speed = speed;

    turns.A = ((0.5*speed.x) - (0.86602540378*speed.y) - (rayon_robot*speed.rot)) * motor_ratio;
    turns.B = ((0.5*speed.x) + (0.86602540378*speed.y) - (rayon_robot*speed.rot)) * motor_ratio;
    turns.C = ((-1.0*speed.x)  - (rayon_robot*speed.rot)) * motor_ratio;

    stepperA.setSpeed(turns.A);
    stepperB.setSpeed(turns.B);
    stepperC.setSpeed(turns.C);
}

void SpeedController::testWheels(){
    static double pre_time = 0;
    static int state = 0;
    static float speed[6][3] = {{1, 0, 0}, {0, 1, 0}, {0, 0, 1}, {-1, 0, 0}, {0, -1, 0}, {0, 0, -1}};
    if(millis() - pre_time > 1000){
        state = (state + 1)%6;
        stepperA.setSpeed(speed[state][0] * motor_ratio);
        stepperB.setSpeed(speed[state][1] * motor_ratio);
        stepperC.setSpeed(speed[state][2] * motor_ratio);
        pre_time = millis();
    }
}

void SpeedController::run(){
    stepperA.runSpeed();
    stepperB.runSpeed();
    stepperC.runSpeed();
}

void SpeedController::printWeelSpeed(){
    Serial.print("Speed A: ");
    Serial.print(turns.A);
    Serial.print("\t");
    Serial.print("Speed B: ");
    Serial.print(turns.B);
    Serial.print("\t");
    Serial.print("Speed C: ");
    Serial.print(turns.C);
    Serial.println();
}

void SpeedController::printRobotSpeed(){
    Serial.print("Speed A: ");
    Serial.print(turns.A);
    Serial.print("\t");
    Serial.print("Speed B: ");
    Serial.print(turns.B);
    Serial.print("\t");
    Serial.print("Speed C: ");
    Serial.print(turns.C);
    Serial.println();
}

SpeedPolar convertCartToPolar(SpeedCart cart) {
    SpeedPolar polar;
    polar.r = sqrt(cart.x * cart.x + cart.y * cart.y);
    polar.angle = atan2(cart.y, cart.x);
    polar.rot = cart.rot;
    return polar;
}

SpeedCart convertPolarToCart(SpeedPolar polar) {
    SpeedCart cart;
    cart.x = polar.r * cos(polar.angle);
    cart.y = polar.r * sin(polar.angle);
    cart.rot = polar.rot;
    return cart;
}


