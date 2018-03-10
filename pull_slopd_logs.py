import pycurl
import io
from pymongo import MongoClient

import slopd_log_parse

buffer = io.BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://pdreport.slocity.org/policelog/rpcdsum.txt')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue().decode('iso-8859-1')
parsed = slopd_log_parse.parse_log(body)

client = MongoClient('mongodb', 27017)
db = client.snoopy
logs = db.police_logs

for entry in parsed:
	existing = logs.find_one({"report_number": entry["report_number"]})
	if not existing:
		logs.insert(entry)
	else:
		print("skipping, already exists")
