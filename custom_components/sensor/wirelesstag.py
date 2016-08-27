from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    CONF_API_KEY, CONF_PASSWORD, CONF_USERNAME)

import logging
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = [
    'https://github.com/wwidurek/wirelesstag/archive/master.zipsdd'
    '#wirelesstag==0.5.2']

import wirelesstag

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)    
    #_LOGGER.error(
    #        "WOJTEK"+username+"END"+password
    #        )
    dev = []

    authorization = wirelesstag.ClientAuth(username,password)
    tagData = wirelesstag.WirelessTagData(authorization)
    tagList = tagData.tagList 
    for i in tagList:
       tag_uuid=i
       tag_name=tagList[i]["tag_name"]
       dev.append(WirelessTagSensor(tag_name,tag_uuid,tagData))
    add_devices(dev)


class WirelessTagSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self,name,uuid,tagData):
        self._name=name
        self._uuid=uuid
        self._tagData=tagData
        self._state = None
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
        return TEMP_CELSIUS

    def update(self):
        temperature=self._tagData.getTemperature(self._uuid)
        self._state=temperature

