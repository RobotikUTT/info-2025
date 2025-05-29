import qwiic_otos
import time
import math
import sys

def distance_between(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx**2 + dy**2)

def main():
    myOtos = qwiic_otos.QwiicOTOS()

    if not myOtos.is_connected():
        print("Le capteur OTOS n'est pas connecté.", file=sys.stderr)
        return

    myOtos.begin()

    print("Placez le capteur à plat et ne bougez pas pendant la calibration...")
    for i in range(5, 0, -1):
        print(f"Calibration dans {i} secondes...")
        time.sleep(1)

    print("Calibration de l'IMU en cours...")
    myOtos.calibrateImu()

    myOtos.setLinearUnit(myOtos.kLinearUnitMeters)
    myOtos.setAngularUnit(myOtos.kAngularUnitRadians)
    myOtos.resetTracking()

    start_pos = myOtos.getPosition()
    last_pos = start_pos
    total_distance = 0.0

    print("Suivi en cours... (CTRL+C pour quitter)")
    try:
        while True:
            current_pos = myOtos.getPosition()
            dist = distance_between(last_pos, current_pos)
            total_distance += dist
            last_pos = current_pos

            # Affiche la distance en centimètres
            print(f"Distance totale parcourue : {total_distance * 100:.2f} cm")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nArrêt du suivi.")

if __name__ == "__main__":
    main()
