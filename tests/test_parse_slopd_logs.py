import unittest
import slopd_log_parse

class TestParseSLOPDLogs(unittest.TestCase):
	def test_parse_log_address(self):
		sample_file = open('tests/sample_slopd_log.txt', 'r')
		sample_log = sample_file.read()
		parsed = slopd_log_parse.parse_log(sample_log)
		for entry in parsed:
				self.assertIn('address', entry)
		sample_file.close()

	def test_parse_date_and_time(self):
		entry = self.get_first_entry()
		print(entry["date"])
		self.assertEqual('09/07/17', entry["date"])

	def get_first_entry(self):
		sample_file = open('tests/sample_slopd_log.txt', 'r')
		sample_log = sample_file.read()
		parsed = slopd_log_parse.parse_log(sample_log)
		return parsed[0]
