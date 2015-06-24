Ride On Time
===

Parsing GTFS for great justice!

Installation
---

* Clone from develop
* `cd` into the directory and `pip install -r requirements.txt`
* Export a secret key, like so `export RIDEONTIME_SECRET_KEY='when is the bus getting here?'`
* `project/manage.py check`
* `project/manage.py test`
* `project/manage.py syncdb`
* `project/manage.py runserver`
* Visit [http://localhost:8000/admin](http://localhost:8000/admin)
