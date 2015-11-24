# from selenium.webdriver.common.by import By
# 
# '''This defines web objects by page name'''
# 
# 
# class MaternalEligibilityFinder(object):
#     HEADING = (By.TAG_NAME, 'body')
#     DATE = (By.NAME, 'report_datetime_0')
#     TIME = (By.NAME, 'report_datetime_1')
#     PARTICIPANT_AGE = (By.ID, 'id_age_in_years')
#     PREGNANCY = (By.ID, 'id_currently_pregnant_0')
#     SUBMIT = (By.NAME, '_save')
# 
# 
# class ConsentFinder(object):
#     FIRST_NAME = (By.NAME, 'first_name')
#     LAST_NAME = (By.ID, 'id_last_name')
#     INITIALS = (By.ID, 'id_initials')
#     LANGUAGE = (By.ID, 'id_language_1')
#     LITERACY = (By.ID, 'id_is_literate_0')
#     CONSENT_DATE = (By.CSS_SELECTOR, "a[href*='javascript:DateTimeShortcuts.handleCalendarQuickLink(0, 0);']")
#     CONSENT_TIME = (By.CSS_SELECTOR, "a[href*='javascript:DateTimeShortcuts.handleClockQuicklink(0, -1);']")
#     GENDER = (By.ID, 'id_gender_1')
#     DOB = (By.ID, 'id_dob')
#     DOB_EST = (By.ID, 'id_is_dob_estimated_0')
#     CITIZEN = (By.ID, 'id_citizen_0')
#     OMANG_ID = (By.ID, 'id_identity')
#     ID_TYPE = (By.ID, 'id_identity_type_0')
#     CONFIRM_OMANG_ID = (By.ID, 'id_confirm_identity')
#     SUBMIT = (By.NAME, '_save')
# 
# 
# class SampleConsentFinder(object):
#     SAMPLE_CONSENT_LANGUAGE = (By.CSS_SELECTOR, "input[id='id_language_1']")
#     SAMPLE_STORAGE = (By.ID, 'id_may_store_samples_0')
#     IS_LITERATE = (By.ID, 'id_is_literate_0')
#     CONSENT_BENEFITS = (By.ID, 'id_consent_benefits_0')
#     SUBMIT = (By.NAME, '_save')
