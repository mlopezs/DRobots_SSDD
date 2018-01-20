// -*- mode:c++ -*-
#include "drobots.ice"

module comunication {

struct DetectorWarning{
  int nRobots;
  drobots::Point location;
};

struct Objective{
  int direccion;
  int distancia;
  int prioridad;
};

struct DetectionScanner{
  int direccion;
  int aperturaEscaner;
  int numeroEncontrado;
};

  interface Estado {
    void sendStatus(drobots::Point posicion, int containerNumber, int id);
  };

  interface SeeingController extends drobots::RobotController, Estado {
    void agregarEstado(int id, drobots::Point location);
  };

  interface OffensiveController extends drobots::RobotController, Estado {
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
