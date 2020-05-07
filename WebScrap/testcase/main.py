import unittest
from selenium import webdriver
import page

class PythonOrgSearch(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome("C:\Program Files (x86)/chromedriver.exe")
		driver.get("http://www.python.org")

	def title_search_python(self):
		mainPage = patge.MainPAge(self.driver)
		assert mainPage.is_title_matches()
		mainPage.search_text_element = "pycon"
		mainPage.click_go_button()
		search_result_page = page.SearchResultPage(self.driver)
		assert search_result_page.is_results_found()


	# def test_example(self):
	# 	assert True

	# def test_title(self):
	# 	mainPage = page.MainPage()
	# 	assert mainPage.is_title_matches()

	# def test_example_2(self):
	# 	assert False

	def tearDown(self):
		self.driver.close()


if __name__ == "__main__":
	unittest.main()