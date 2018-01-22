// -*- mode:c++ -*-

#include "drobots.ice"

module communication {

struct DetectorWarning{
  int nRobots;
  drobots::Point location;
};

struct DetectionScanner{
  int direccion;
  int aperturaEscaner;
  int numeroEncontrado;
};

struct Objective{
  bool prioridad;
  drobots::Point posAtacante;
  drobots::Point posObjetivo;
  int direccion;
  double distancia;
};

  interface State {
    void sendStatus(drobots::Point posicion);
  };

  interface WatcherController extends drobots::RobotController, State {
    void addState(drobots::Point location);
  };

  interface AttackerController extends drobots::RobotController, State {
    void destroyTarget(Objective objective);
    void markTarget(int direccion, drobots::Point location);
    void receiveObjectives(Objective objective);
    void receiveAlert(DetectorWarning detectorWarningMonger);
    void addState(drobots::Point location);
  };

  interface WarningController {
    void sendWarning(int detectedRobots, drobots::Point location);
  };

};
