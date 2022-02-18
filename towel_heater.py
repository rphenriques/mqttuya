# -*- coding: utf-8 -*-
"""
 MQTTuya - Towel Heater Wrapper

 Author: Rui Pedro Henriques
 For more information see https://github.com/rphenriques/mqttuya

"""
import tinytuya


class TowelHeaterDevice(tinytuya.Device):
    """
    Represents a Tuya based Towel Heater
    Args:
        dev_id (str): The device id.
        address (str): The network address.
        local_key (str): The encryption key. Defaults to None.
    """

    def __init__(self, dev_id, address, local_key, dev_type="default"):
        super(TowelHeaterDevice, self).__init__(dev_id, address, local_key, dev_type)

    def turn_on(self):
        """Turn the device on"""
        payload=self.generate_payload(tinytuya.CONTROL, {'1': True})
        data = self._send_receive(payload)
        return data

    def turn_off(self):
        """Turn the device on"""
        #TODO: reset timer before tunrning off
        payload=self.generate_payload(tinytuya.CONTROL, {'1': False})
        data = self._send_receive(payload)
        return data

    def lock(self):
        """Child lock the device"""
        payload=self.generate_payload(tinytuya.CONTROL, {'2': True})
        data = self._send_receive(payload)
        return data

    def unlock(self):
        """Child unlock the device"""
        payload=self.generate_payload(tinytuya.CONTROL, {'2': False})
        data = self._send_receive(payload)
        return data

    def set_temp(self, target_temp):
        """
        Set target temp

        Args:
            target_temp(int): target_temp to set
        """
        payload=self.generate_payload(tinytuya.CONTROL, {'3': target_temp})
        data = self._send_receive(payload)
        return data

    def set_timer(self, minutes):
        """
        Set device timer

        Args:
            minutes(int): target_temp to set
        """
        #TODO: check if minutes is valid
        payload=self.generate_payload(tinytuya.CONTROL, {'5': minutes})
        data = self._send_receive(payload)
        return data

    def timer_off(self):
        """Reset device timer"""
        payload=self.generate_payload(tinytuya.CONTROL, {'5': 0})
        data = self._send_receive(payload)
        return data

    def open(self):
        """Set device "open" state"""
        payload=self.generate_payload(tinytuya.CONTROL, {'111': 'High'})
        data = self._send_receive(payload)
        return data

    def close(self):
        """Set device "close" state"""
        payload=self.generate_payload(tinytuya.CONTROL, {'111': 'Low'})
        data = self._send_receive(payload)
        return data

    def get_data(self):
        """Get "translated" status from device"""
        aux_status = self.status()
        if 'dps' not in data:
            return None
        data = {'state': 'ON' if aux_status['dps']['1'] else 'OFF',
                'lock': 'LOCKED' if aux_status['dps']['2'] else 'UNLOCKED',
                'target_temp': aux_status['dps']['3'],
                'current_temp': aux_status['dps']['4'],
                'timer': aux_status['dps']['5'],
                'open': 'OPEN' if aux_status['dps']['111'] == 'High' else 'CLOSED'}
        return data
