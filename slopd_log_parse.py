import re
import pprint
import datetime
import time

def parse_log(log_contents):
	separator = '={79}\s\n'
	expression = separator
	lines = re.split(expression, log_contents)
	combined = combine_header_body(lines)
	return map(parse_entry, combined)

def parse_entry(line):
	entry = {'raw': line}

	report_num_pattern          = re.compile("([0-9]+)\s")
	date_pattern                = re.compile("[0-9]+\s([0-9\/]+)\s")
	received_pattern            = re.compile("Received:([0-9]{2}:[0-9]{2})\s")
	dispatched_pattern          = re.compile("Dispatched:([0-9]{2}:[0-9]{2})\s")
	arrived_pattern             = re.compile("Arrived:([0-9]{2}:[0-9]{2})\s")
	cleared_pattern             = re.compile("Cleared:([0-9]{2}:[0-9]{2})\s")
	type_pattern                = re.compile("Type:\s*([a-zA-Z0-9]+)")
	location_pattern            = re.compile("Location:(\S*)")
	address_pattern             = re.compile("Addr: (.*)Clearance Code")
	grid_pattern                = re.compile("; GRID (.*)(,|;)")
	clearance_code_pattern      = re.compile("Clearance Code: (\S*)\s")
	responsible_officer_pattern = re.compile("Responsible Officer: (\S*, .)")
	call_comments_pattern       = re.compile("CALL COMMENTS: (.*)\n")
	description_pattern         = re.compile("Des:(.*)incid")

	match = report_num_pattern.match(line)
	if match:
		entry["report_number"] = match.group(1)
	match = date_pattern.match(line)
	if match:
		dateString = match.group(1)
		entry["date"] = dateString
		split = re.split("\/", dateString)
		date = datetime.datetime(int(split[2]), int(split[0]), int(split[1]))
		timestamp = time.mktime(date.timetuple())
		entry["timestamp"] = timestamp
	search = received_pattern.search(line)
	if search:
		entry["received"] = search.group(1)
	search = dispatched_pattern.search(line)
	if search:
		entry["received"] = search.group(1)
	search = arrived_pattern.search(line)
	if search:
		entry["arrived"] = search.group(1)
	search = cleared_pattern.search(line)
	if search:
		entry["cleared"] = search.group(1)
	search = type_pattern.search(line)
	if search:
		entry["type"] = search.group(1)
	search = location_pattern.search(line)
	if search:
		entry["location"] = search.group(1)
	search = address_pattern.search(line)
	if search:
		address_line = search.group(1)
		address_sections = re.split(";", address_line)
		entry["address"] = address_sections[0]
	search = clearance_code_pattern.search(line)
	if search:
		entry["clearance_code"] = search.group(1)
	search = responsible_officer_pattern.search(line)
	if search:
		entry["responsible_officer"] = search.group(1)
	search = call_comments_pattern.search(line)
	if search:
		entry["call_comments"] = search.group(1)
	search = description_pattern.search(line)
	if search:
		entry["description"] = search.group(1)

	return entry

# It's hard to split on every nth occurence so splitting up the header and
# body and then recombining is how I decided to shortcut that.
def combine_header_body(lines):
	combined_lines = []
	current_entry = ""
	for line in lines:
		body_pattern = re.compile("Type: (\S*)\s")
		header_pattern = re.compile(".*Received:.*Dispatched:")
		body_match = body_pattern.match(line)
		header_match = header_pattern.match(line)
		if body_match:
			current_entry = current_entry + line
			combined_lines.append(current_entry)
		elif header_match:
			current_entry = line

	return combined_lines
