=====
sumdb
=====

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/OpenTransitTools/gtfsdb
   :target: https://gitter.im/OpenTransitTools/gtfsdb?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


* SQLAlchemy ORM for carshare, bikeshare, etc... data
* Controller code that exposes SUM position data in a geojson format.
* Pyramid service that exposes the geojson data as a webservice.
* Relationship mapping between GTFS and SUM data (e.g., what SUM vehicles are near stop X)
* To get started:
 - PRE: have access to SUM data, which might require license keys and approval from 3rd parties
 - git clone https://github.com/OpenTransitTools/sumdb.git
 - cd sumdb/
 - buildout
 - bin/loader
 - bin/pserve development.ini
 - http://localhost:31113/static/test.html
 
* Carshare Data
 - car2go
 - ReachNow
 - Zipcar
 - Bikeshare (BIKETOWN in Portland)
 - Uber and Lyft
 - etc...
