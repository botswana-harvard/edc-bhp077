import time

from getresults.tests.base_selenium_test import BaseSeleniumTest


class TestReceiveSelenium(BaseSeleniumTest):

    def test_open_receive(self):
        '''Asserts user can open receive sample window'''
        self.login()
        self.assertTrue('Receive', self.browser.title)
        self.browser.save_screenshot('getresults_receive/screenshots/receive.png')

    def test_open_receive_sample_modal(self):
        '''Asserts user can open receive sample window'''
        self.login()
        time.sleep(1)
        receive = self.browser.find_element_by_name("topbar_receive")
        receive.click()
        time.sleep(1)
        self.assertTrue('Receive', self.browser.title)
        sample_button = self.browser.find_element_by_name("submit_button")
        sample_button.click()
        time.sleep(1)
        self.browser.save_screenshot('getresults_receive/screenshots/receive_sample.png')

    def test_open_receive_batch_modal(self):
        '''Asserts user can open receive sample window'''
        self.login()
        time.sleep(1)
        receive = self.browser.find_element_by_name("topbar_receive")
        receive.click()
        time.sleep(1)
        self.assertTrue('Receive', self.browser.title)
        sample_button = self.browser.find_element_by_name("receive_batch")
        sample_button.click()
        time.sleep(1)
        self.browser.save_screenshot('getresults_receive/screenshots/receive_batch.png')

    def test_open_batch_preset_form(self):
        '''Asserts user can open the batch preset form'''
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/receive/')
        time.sleep(1)
        batch_preset_button = self.browser.find_element_by_id("receive_batch_button")
        batch_preset_button.click()
        time.sleep(1)
        self.switch_to_new_window('Batch Preset Form', 'batchModalLabel')

    def test_submit_batch_preset_form_with_only_itemcount_populated(self):
        '''Asserts user can open the batch preset form and submit it with all defaults populated'''
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/receive/')
        time.sleep(1)
        batch_preset_button = self.browser.find_element_by_id("receive_batch_button")
        batch_preset_button.click()
        time.sleep(1)
        self.switch_to_new_window('Batch Preset Form', 'batchModalLabel')
        itemcount_input = self.browser.find_element_by_id("item_count_input_id")
        itemcount_input.send_keys(10)
        batch_preset_submit = self.browser.find_element_by_id("submit_batch_preset")
        batch_preset_submit.click()
        number_rows = self.browser.find_elements_by_name("patient_name")
        self.assertEqual(len(number_rows), 10)

    def test_submit_batch_preset_form_with_all_defaults_populated(self):
        '''Asserts user can open the batch preset form and submit it with only item count'''
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/receive/')
        time.sleep(1)
        batch_preset_button = self.browser.find_element_by_id("receive_batch_button")
        batch_preset_button.click()
        time.sleep(1)
        self.switch_to_new_window('Batch Preset Form', 'batchModalLabel')
        itemcount_input = self.browser.find_element_by_id("item_count_input_id")
        itemcount_input.send_keys(5)
        sampletype_input = self.browser.find_element_by_id("sample_type_input_id")
        sampletype_input.send_keys('BF')
        sitecode_input = self.browser.find_element_by_id("site_code_input_id")
        sitecode_input.send_keys('14')
        protocol_input = self.browser.find_element_by_id("protocol_number_input_id")
        protocol_input.send_keys('066')
        batch_preset_submit = self.browser.find_element_by_id("submit_batch_preset")
        batch_preset_submit.click()
        time.sleep(1)
        receive_sample_type_name = self.browser.find_elements_by_name("sample_type_name")[0]
        self.assertEqual(receive_sample_type_name.get_attribute('value'), 'BF')
        receive_site_code_name = self.browser.find_elements_by_name("site_code_name")[0]
        self.assertEqual(receive_site_code_name.get_attribute('value'), '14')
        receive_protocol_no_name = self.browser.find_elements_by_name("protocol_no_name")[0]
        self.assertEqual(receive_protocol_no_name.get_attribute('value'), '066')

    def test_user_batch_filter(self):
        self.login()
        time.sleep(1)
        self.browser.find_element_by_name("topbar_receive").click()
        time.sleep(1)
        self.browser.find_element_by_id('receive_batch_button').click()
        time.sleep(1)
        self.switch_to_new_window('Batch Preset Form', 'batchModalLabel')
        self.browser.find_element_by_id('item_count_input_id').send_keys(1)
        time.sleep(1)
        self.browser.find_element_by_id("submit_batch_preset").click()
        time.sleep(1)
        self.browser.find_element_by_name("topbar_receive").click()
        self.browser.find_element_by_name('view_my_batches').click()
        time.sleep(1)
        self.assertIn('receive_user_batches', self.browser.current_url)
        table = self.browser.find_element_by_class_name('table-responsive')
        rows = table.find_elements_by_tag_name('th')
        self.assertTrue(any(row.text == 'Batch Identifier' for row in rows))
        self.browser.save_screenshot('getresults_receive/screenshots/receive_user_batch.png')

