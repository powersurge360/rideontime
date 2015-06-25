Ride On Time
===

Parsing GTFS for great justice!

Prerequisites
---
* PostGIS
* GeoDjango

Installation
---

* Clone from develop
* `cd` into the directory and `pip install -r requirements.txt`
* Copy `project/rideontime/dotenv` to `project/rideontime/.env` and fill in
the applicable variables.
* `project/manage.py check`
* `project/manage.py test`
* `project/manage.py syncdb`

Running the App
---
* `project/manage.py runserver`
* Visit [http://localhost:8000/admin](http://localhost:8000/admin)
