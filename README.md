# mqttuya

[![License](https://img.shields.io/github/license/rphenriques/mqttuya)](https://img.shields.io/github/license/rphenriques/mqttuya)

Python module to interface with Tuya WiFi smart devices. 

## Description

This is a wraper module around TinyTuya to extend it's funcionality to CREATE's Warm Towel Crystal Towel Heater https://www.create-store.com/pt/comprar-toalheiro-eletrico/72182-warm-towel-cristal-toalheiro-eletrico-de-vidro-com-wiffi.html and interface it with MQTT.

## Tuya Data Points - DPS Table

### Version 3.3 - Towel Heater 
| DP ID        | Function Point | Type        | Range       | Units |
| ------------- | ------------- | ------------- | ------------- |------------- |
|1|Heater switch|bool|True/False|n/a|
|2|Child lock|bool|True/False|n/a|
|3|Target temperature|integer|5-40|ºC|
|4|Current temperature|integer|n/a|ºC|
|5|Timer|integer|0-1440|min|
|111|Open Close|enum|High, Low|n/a|

The function of "Open Close" DP is not very clear, but if set to Close ("Low") the heater does not warm up even if switched ON

## Credits

  * TinyTuya https://github.com/jasonacox/tinytuya by jasonacox.
  
## Related Projects

  * https://github.com/TradeFace/tuyaface - Python Async Tuya API
