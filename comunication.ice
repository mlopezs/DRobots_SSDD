// -*- mode:c++ -*-
#include "drobots.ice"

module comunication {

struct warning{
  int nRobots;
  drobots::Point location;
};

struct objetivo{
  int direccion;
  int distancia;
};

  interface Estado {
    void sendStatus(drobots::Point posicion, int containerNumber, int id);
  };

  interface SeeingController extends drobots::RobotController, Estado {
    void agregarEstado(int id, drobots::Point location);
  };

  interface OffensiveController extends drobots::RobotController, Estado {
    void destroyAnything(objetivo objective);
    void ola(int entero1, int entero2);
  };

  interface WarningController {
    void sendWarning();
  };

};
