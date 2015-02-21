import requests
import time
from splinter import Browser
import shutil
import process



def download(file_name):
	url = 'http://pandemaniac.bkspin.com/login'
	file_url = 'http://pandemaniac.bkspin.com/submit/{}/download'.format(file_name)
	payload = {'username': 'Red_Mansion',
				'password': 'datuidatui'}

	s = requests.Session()
	s.post(url, payload)
	response = s.get(file_url, stream=True)

	fout_name = file_name+'.json'
	with open(fout_name, 'wb') as fout:
		shutil.copyfileobj(response.raw, fout)
	del response

	print('Successfully download to {}'.format(fout_name))

def upload():
	url = 'http://pandemaniac.bkspin.com/login'
	with Browser() as browser:
		browser.visit(url)
		browser.fill('username', 'Red_Mansion')
		browser.fill('password', 'datuidatui')

		browser.find_by_value('Log In').click()
		browser.click_link_by_href('/submit')
		browser.click_link_by_text(file_name)
		browser.click_link_by_text('Upload')
		browser.find_by_xpath('html/body/div[3]/div[3]/div[2]/form/div/div[1]/div/div/div/span/span/input').click()

		time.sleep(300)



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('f_name', default='2.5.01')
	args = parser.parse_args()
	file_name = args.f_name

	download(file_name)
	process.process_file(file_name+'.json')
	upload()





