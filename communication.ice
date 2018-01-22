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

  interface State {
    void sendStatus(drobots::Point posicion, int containerNumber, int id);
  };

  interface WatcherController extends drobots::RobotController, Estado {
    void agregarEstado(int id, drobots::Point location);
  };

  interface AttackerController extends drobots::RobotController, Estado {
    void destroyAnything(Objective objective);
    void markTarget(int direccion, drobots::Point location);
    void receiveObjectives(int listaObjetivos);
    void receiveAlert(DetectorWarning detectorWarningMonger);
    void agregarEstado(int id, drobots::Point location);
  };

  interface WarningController {
    void sendWarning(int detectedRobots, drobots::Point location);
  };

};
