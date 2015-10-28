import time

from selenium.webdriver.common.keys import Keys

from .base_selenium_test import BaseSeleniumTest


class TestAdminFormsInfant(BaseSeleniumTest):

    def login_navigate_to_admin(self):
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/admin/microbiome/')

    def test_infant_birth_admin(self):
        self.login_navigate_to_admin()
        time.sleep(1)
        self.browser.find_element_by_link_text('Infant Birth Feeding & Vaccinations').click()
        time.sleep(1)
        self.assertIn('infantbirthfeedvaccine/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_birth_admin.png')

    def test_infant_birth_arv_admin(self):
        self.login_navigate_to_admin()
        time.sleep(1)
        self.browser.find_element_by_link_text('Infant Birth Record: ARVs').click()
        time.sleep(1)
        self.assertIn('infantbirtharv/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_birth_arv_admin.png')

    def test_infant_birth_exam_admin(self):
        self.login_navigate_to_admin()
        time.sleep(1)
        self.browser.find_element_by_partial_link_text('Infant Birth Record: Exams').click()
        time.sleep(1)
        self.assertIn('infantbirthexam/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infact_birth_exam_admin.png')

    def test_infant_birth_records(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_partial_link_text('Infant Birth Records').click()
        time.sleep(1)
        self.assertIn('infantbirth/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infact_birth_records.png')

    def test_infant_congenital_anomalies_cardio(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_partial_link_text('Infant Congenital Anomalies:Cardios').click()
        time.sleep(1)
        self.assertIn('infantcardiovasculardisorderitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_cardio.png')

    def test_infant_congenital_anomalies_cleft(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_partial_link_text('Infant Congenital Anomalies:Cleft').click()
        time.sleep(1)
        self.assertIn('infantcleftdisorderitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_cleft.png')

    def test_infant_congenital_anomalies_cns(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Cnss').click()
        time.sleep(1)
        self.assertIn('infantcnsabnormalityitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_cns.png')

    def test_infant_congenital_anomalies_facial(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Facials').click()
        time.sleep(1)
        self.assertIn('infantfacialdefectitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_facials.png')

    def test_infant_congenital_anomalies_femalegen(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:FemaleGens').click()
        time.sleep(1)
        self.assertIn('infantfemalegenitalanomalyitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_femalegen.png')

    def test_infant_congenital_anomalies_malegen(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:MaleGens').click()
        time.sleep(1)
        self.assertIn('infantmalegenitalanomalyitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_malegen.png')

    def test_infant_congenital_anomalies_lower_gast(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:LowerGasts').click()
        time.sleep(1)
        self.assertIn('infantlowergastrointestinalitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_lower_gast.png')

    def test_infant_congenital_anomalies_mouth(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:MouthUpps').click()
        time.sleep(1)
        self.assertIn('infantmouthupgastrointestinalitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_mouth.png')

    def test_infant_congenital_anomalies_muscle(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Musculosks').click()
        time.sleep(1)
        self.assertIn('infantmusculoskeletalabnormalitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_muscle.png')

    def test_infant_congenital_anomalies_renal(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Renals').click()
        time.sleep(1)
        self.assertIn('infantrenalanomalyitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_renal.png')

    def test_infant_congenital_anomalies_respiratory(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Respitarorys').click()
        time.sleep(1)
        self.assertIn('infantrespiratorydefectitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_respiratory.png')

    def test_infant_congenital_anomalies_skin(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Skins').click()
        time.sleep(1)
        self.assertIn('infantskinabnormalitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_skin.png')

    def test_infant_congenital_anomalies_triome(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomalies:Trisomess').click()
        time.sleep(1)
        self.assertIn('infanttrisomieschromosomeitems/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anom_triome.png')

    def test_infant_congenital_anomalies(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Congenital Anomaliess').click()
        time.sleep(1)
        self.assertIn('infantcongenitalanomalies/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_congenital_anomalies.png')

    def test_infant_death(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Deaths').click()
        time.sleep(1)
        self.assertIn('infantdeath/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_death.png')

    def test_infant_eligibility(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Eligibility').click()
        time.sleep(1)
        self.assertIn('infanteligibility/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_eligibility.png')

    def test_infant_visit(self):
        self.login_navigate_to_admin()
        self.browser.find_element_by_link_text('Infant Visits').click()
        time.sleep(1)
        self.assertIn('infantvisit/', self.browser.current_url)
        self.browser.get(self.browser.current_url + 'add/')
        self.browser.save_screenshot('microbiome/screenshots/infant_visit.png')