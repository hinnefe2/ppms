"""Module containing a class to interface with a Quantum Dynamics PPMS DynaCool"""

# requires Python for .NET
# can be installed with 'pip install pythonnet'

import clr

# load the C# .dll supplied by Quantum Design
try:
    clr.AddReference('QDInstrument')
except:
    if clr.FindAssembly('QDInstrument') is None:
        print('Could not find QDInstrument.dll')
    else:
        print 'Found QDInstrument.dll at {}'.format(clr.FindAssembly('QDInstrument')
        print 'Try right-clicking the .dll, selecting 'Properties', and then clicking "Unblock"'

# import the C# classes for interfacing with the PPMS
from QuantumDesign.QDInstrument import *

    

QDI_DYNACOOL_TYPE = QDInstrumentBase.QDInstrumentType.DynaCool
DEFAULT_PORT = 11000
QDI_FIELD_STATUS = ['MagnetUnknown',
      'StablePersistent',
      'WarmingSwitch',
      'CoolingSwitch',
      'StableDriven',
      'Iterating',
      'Charging',
      'Discharging',
      'CurrentError',
      'Unused9',
      'Unused10',
      'Unused11',
      'Unused12',
      'Unused13',
      'Unused14',
      'MagnetFailure']
QDI_TEMP_STATUS = ['TemperatureUnknown',
      'Stable',
      'Tracking',
      'Unused3',
      'Unused4',
      'Near',
      'Chasing',
      'Filling',
      'Unused8',
      'Unused9',
      'Standby',
      'Unused11',
      'Unused12',
      'Disabled',
      'ImpedanceNotFunction',
      'TempFailure']



class Dynacool:
    """Thin wrapper around the QuantumDesign.QDInstrument.QDInstrumentBase class"""

    def __init__(self, ip_address):
       self.qdi_instrument = QDInstrumentFactory.GetQDInstrument(QDI_DYNACOOL_TYPE, True, ip_address, DEFAULT_PORT)

    def getTemperature(self):
        """Return the current temperature, in Kelvin."""
        return self.qdi_instrument.GetTemperature(0,0)

    def setTemperature(self, temp, rate):
        """Set the temperature.

            Keyword arguments:
            temp -- the temperature in Kelvin
            rate -- the cooling / heating rate, in K / min
            """
        return self.qdi_instrument.SetTemperature(temp, rate, 0)

    def waitForTemperature(self, delay=5, timeout=600):
        """Pause execution until the PPMS reaches the temperature setpoint."""
        return self.qdi_instrument.WaitFor(True, False, False, False, delay, timeout)

    def getField(self):
        """Return the current field, in gauss."""
        return self.qdi_instrument.GetField(0,0)

    def setField(self, field, rate):
        """Set the field.

            Keyword arguments:
            field -- the field, in gauss
            rate  -- the field sweep rate, in gauss / second
            """
        return self.qdi_instrument.SetField(field, rate, 'Linear', 'Persistent')

    def waitForField(self, delay=5, timeout=600):
        """Pause execution until the PPMS reaches the field setpoint."""
        return self.qdi_instrument.WaitFor(False, True, False, False, delay, timeout)
