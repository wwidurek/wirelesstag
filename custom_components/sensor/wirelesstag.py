from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    CONF_API_KEY, CONF_PASSWORD, CONF_USERNAME)
import logging
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

SENSOR_TEMPERATURE = 'Temperature'
SENSOR_HUMIDITY = 'Humidity'
SENSOR_VOLTAGE = 'Voltage'
SENSOR_TYPES = {
    SENSOR_TEMPERATURE: ['Temperature', TEMP_CELSIUS],
    SENSOR_HUMIDITY: ['Humidity', '%'],
    SENSOR_VOLTAGE: ['Voltage', 'V']
}

REQUIREMENTS = [
		'https://github.com/wwidurek/wirelesstag/archive/master.zip'
		'#wirelesstag==0.5.2']


MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=300)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    import wirelesstag
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)    
    
    dev = []

    authorization = wirelesstag.ClientAuth(username,password)
    tagData = wirelesstag.WirelessTagData(authorization)
    tagList = tagData.tagList 
    for i in tagList:
       tag_uuid=i
       tag_name=tagList[i]["tag_name"]
       for variable in config['monitored_conditions']:
          if variable not in SENSOR_TYPES:
            _LOGGER.error('Sensor type: "%s" does not exist', variable)
          else:
            dev.append(WirelessTagSensor(tag_name,tag_uuid,tagData,SENSOR_TYPES[variable][0]))

    add_devices(dev)


class WirelessTagSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self,name,uuid,tagData,sensor_type):
        self._name=name
        self._uuid=uuid
        self._tagData=tagData
        self._state = None
        self._sensor_type=sensor_type
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name 

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state 

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement 

    def update(self):
        if self._sensor_type == SENSOR_TEMPERATURE:
          self._state=self._tagData.getTemperature(self._uuid)
        elif self._sensor_type == SENSOR_HUMIDITY:
          self._state=self._tagData.getHumidity(self._uuid)
        elif self._sensor_type == SENSOR_VOLTAGE:
          self._state=self._tagData.getBatteryVolt(self._uuid) 
        else:
          _LOGGER.error('Sensor type: "%s" does not exist', self._sensor_type)

