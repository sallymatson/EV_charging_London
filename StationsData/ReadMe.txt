**Stations dataset**

Geolocation coordinates of charging points. The data is semi-structured in csv. 

It provides attributes of 2,024 charging points located in the Greater London Area.

Dataset fields:
- identifier of the charging point
- latitude of the charging point
- longitude of the charging point
- identifier of the charging point as per the relevant public charging network provider
- postcode of the charging point

**Sockets dataset**

Information about the sockets of charging point stations. The data is semi-structured in csv.

It provides attributes of 4,084 sockets. 

Dataset fields:
- identifier of the socket
- socket type
- socket power
- identifier of the charging station with which the socket is associated


**SocketStatus dataset**

Records of the status of sockets over a month from 01/01/2020 00:00:40 to 31/01/2020 23:58:33. The data is semi-structured in csv.

Dataset fields:
- record ID
- record date
- record time
- socket status (1: available; 0: charging; -1: out-of-service)
- socket identifier