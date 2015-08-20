AUTOPSY_SOURCE = (
    ('mother', 'Mother of infant'),
    ('family_mem', 'Other family member'),
    ('hlth_prof', 'Health Professional who cared for the infant'),
    ('med_rec', 'Medical records'),
    ('OTHER', 'Other'),
)

AUTOPSY_SIGNS = (
    ('fever', 'Fever'),
    ('poor_feeding', 'Poor feeding'),
    ('weight_loss', 'Weight loss'),
    ('weakness', 'Weakness'),
    ('stiff_neck', 'Stiff Neck'),
    ('unusual_sleepiness', 'Unusual sleepiness'),
    ('convulsions', 'Convulsions'),
    ('bleeding', 'Bleeding'),
    ('cough', 'Cough'),
    ('diffic_breathing', 'Difficulty breathing'),
    ('swollen_stomach', 'Swollen stomach'),
    ('Vomiting', 'Vomiting'),
    ('diarrhea', 'Diarrhea'),
    ('blood_pus_stool', 'Blood or pus in stool'),
    ('rash_body', 'Rash on body'),
    ('rash_mouth', 'Rash or sores in mouth'),
    ('yellow_eyes_skin', 'Yellow eyes or skin'),
    ('accident', 'Accident'),
    ('infection_genitals', 'Local infection (genitals)'),
    ('infect_other_area', 'Local infection (other than genitals'),
)

FEEDING_CHOICES = (
    ('Breastfeeding only', 'Breastfeeding only'),
    ('Formula feeding only', 'Formula feeding only'),
    ('Both breastfeeding and formula feeding', 'Both breastfeeding and formula feeding'),
    ('Medical complications: Infant did not feed', 'Medical complications: Infant did not feed'),
)

COWS_MILK = (
    ('boiled', '1. Boiled from cow'),
    ('unboiled', '2. Unboiled from cow'),
    ('store', '3. From store'),
    ('N/A', 'Not Applicable'),
)

CTX_PLACEBO_STATUS = (
    ('No modification', 'No modifications made to CTX/Placebo since the last scheduled visit or today'),
    ('Starting CTX/Placebo today', 'Starting CTX/Placebo today or since the last scheduled visit'),
    ('Permanently discontinued', 'Permanently discontinued CTX/Placebo at or before last scheduled visit'),
    ('Never started', 'Never started CTX/Placebo'),
    ('Change in CTX/Placebo since the last scheduled visit or today', 'Change in CTX/Placebo since the last scheduled visit or today (dose modification, permanent discontinuation, temporary hold, resumption / initiation after temporary hold)'),
)

DX_INFANT = (
    ('Pneumonia, suspected (no CXR or microbiologic confirmation)', 'Pneumonia, suspected (no CXR or microbiologic confirmation)'),
    ('Pneumonia, CXR confirmed, no bacterial pathogen', 'Pneumonia, CXR confirmed, no bacterial pathogen'),
    ('Pneumonia, CXR confirmed, bacterial pathogen isolated (specify pathogen)', 'Pneumonia, CXR confirmed, bacterial pathogen isolated (specify pathogen)'),
    ('Pulmonary TB, suspected(no CXR or microbiologic confirmation)', 'Pulmonary TB, suspected(no CXR or microbiologic confirmation)'),
    ('Pulmonary TB, CXR-confirmed (no microbiologic confirmation)', 'Pulmonary TB, CXR-confirmed (no microbiologic confirmation)'),
    ('Pulmonary TB, smear and/or culture positive', 'Pulmonary TB, smear and/or culture positive'),
    ('Extrapulmonary TB,suspected (no CXR or microbiologic confirmation)', 'Extrapulmonary TB,suspected (no CXR or microbiologic confirmation)'),
    ('Bronchiolitis (not bronchitis)', 'Bronchiolitis (not bronchitis)'),
    ('Hepatitis:Drug related', 'Hepatitis:Drug related (report for Grades 2,3,4)'),
    ('Hepatitis:Traditional medication related', 'Hepatitis:Traditional medication related'),
    ('Hepatitis:Hepatitis A', 'Hepatitis:Hepatitis A'),
    ('Hepatitis:Hepatitis B', 'Hepatitis:Hepatitis B'),
    ('Hepatitis:Other/Unknown', 'Hepatitis:Other/Unknown'),
    ('Sepsis,unspecified', 'Sepsis,unspecified'),
    ('Sepsis,pathogen specified', 'Sepsis,pathogen specified'),
    ('Meningitis,unspecified', 'Meningitis,unspecified'),
    ('Meningitis pathogen specified', 'Meningitis pathogen specified'),
    ('Otitis media', 'Otitis media'),
    ('Appendicitis', 'Appendicitis'),
    ('Cholecystitis/cholanangitis', 'Cholecystitis/cholanangitis'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Acute Renal Failure', 'Acute Renal Failure (Record highest creatinine level if creatine tested outside of the study) '),
    ('Anemia', 'Anemia(Only report grade 3 or 4 anemia based on a lab value drawn outside the study'),
    ('Rash', 'Rash (report for Grades 2,3,4)'),
    ('Trauma/accident', 'Trauma/accident'),
    ('Other abnormallaboratory tests(other than tests listed above or tests done as part of this study),specify test and result', 'Other abnormallaboratory tests(other than tests listed above or tests done as part of this study),specify test and result'),
    ('New congenital abnormality not previously identified?,specify', 'New congenital abnormality not previously identified?,specify and complete "Congenital Anomaly"form'),
    ('Other serious (grade 3 or 4)infection(not listed above),specify', 'Other serious (grade 3 or 4)infection(not listed above),specify'),
    ('Other serious (grade 3 or 4) non-infectious(not listed above),specify', 'Other serious (grade 3 or 4)non-infectious(not listed above),specify'),

)

INFANT_OFF_DRUG_REASON = (
    ('completed protocol', '1. Completion of protocol-required period of study treatment'),
    ('off-study', '2. Participant going off-study for any reason, including death or lost to follow-up'),
    ('toxicity', '3. At Investigator\'s discretion, due to persistent toxicity (confirmed or suspected to be possibly related to study drug)'),
    ('caregiver', '4. Participant\'s mother/caregiver no longer wants child to receive study drug'),
    ('hiv infected', '5. Child is HIV- infected (Open-label CTX indicated)'),
    ('OTHER', '9. Other'),
)

INFANT_VISIT_STUDY_STATUS = (
   ('onstudy rando ondrug', '1. On study/On drug (CTX/Placebo), study medication(s) continuing or temporarily held'),
   ('onstudy rando offdrug', '2. On study/Off drug (CTX/Placebo), study medication(s) permanently discontinued- clinic follow-up continuing'),
   ('onstudy rando notstarteddrug', '3. On study/has not yet started study medication(s)(CTX/Placebo)'),
   ('onstudy rando today', '4. Being randomised today'),
   ('onstudy notrando', '5. On Study / Not yet randomized'),
   ('offstudy', '6. Off study-no further follow-up (including death); use only for last study contact'),
)


OFF_STUDY_REASON = [
    ('not_18', ' 1. Mother of infant found to be less than 18 years of age'),
    ('not_citizen', ' 2. Mother found not be a citizen of Botswana'),
    ('moved', ' 3. Subject will be moving out of study area or unable to stay in study area'),
    ('lost_no_contact', ' 4. Lost to follow-up, unable to locate'),
    ('lost_contacted', ' 5. Lost to follow-up, contacted but did not come to study clinic'),
    ('withdrew_by_mother', ' 6. Mother changed mind and withdrew consent'),
    ('withdrew_by_father', ' 7. Father of baby did not want infant to participate and participant withdrew consent'),
    ('withdrew_by_family', ' 8. Other family member did not want mother/infant to participate and participant withdrew consent'),
    ('mother_died', '9. Mother died after consenting, before infant randomized'),
    ('hiv_pos', '10. Infant found to be HIV-infected'),
    ('ill', '11. Infant diagnosed with medical condition making survival to 18 months unlikely'),
    ('>34_day_old', '12. Infant over 34 days old'),
    ('complete', '13. Completion of protocol required period of time for observation (see Study Protocol for definition of Completion.) [skip to end of form]'),
    ('death', '14. Participant death (complete the DEATH REPORT FORM AF005) (For EAE Reporting requirements see EAE Reporting Manual)'),
    ('OTHER', '99. Other'),
    ]

RANDOMIZATION_MATERNAL_ART_STATUS = (
    ('ON', 'On Haart'),
    ('OFF', 'Off'),
)


RANDOMIZATION_MATERNAL_FEEDING_CHOICE = (
    ('FF', 'Formula'),
    ('BF', 'Breast'),
)

RANDOMIZATION_SITE = (
    ('Molepolole', 'Molepolole'),
    ('Lobatse', 'Lobatse'),
    ('Gaborone', 'Gaborone'),
)

REASON_RCV_FORMULA = (
    ('no milk', '1. Mother did not have enough breast milk'),
    ('back to work', '2. Mother returned to work so unable to breastfeed participant exclusively'),
    ('off HAART', '3. Mother stopped breastfeeding because no longer taking HAART'),
    ('afraid to transmit', '4. Mother stopped because she is afraid she will transmit HIV to the participant even though she\'s taking HAART'),
    ('advised to mix feed', '5. Mother advised to add other food/liquids by partner/family'),
    ('felt to mix feed', '6. Mother felt that baby needed other foods/liquids to be healthy (for babies <= 6 months old)'),
    ('complete per protocol', '7. <Per breastfeeding randomisation, infant is >5 months or >11 months of age and completed breastfeeding per protocol'),
    ('OTHER', '9. Other'),
    ('N/A', 'Not Applicable'),
)

REASON_MISSED_CTX_PLACEBO = (
    ('caregiver forgot', 'Caregiver forgot to give the CTX/Placebo'),
    ('caregiver ran out/lost', 'Caregiver ran out of CTX/Placebo or lost the bottle'),
    ('caregiver away', 'Primary caregiver was away from home and did not have another person give the CTX/Placebo'),
    ('infant away', 'Infant was away from home and the CTX/Placebo bottle was not at the other location'),
    ('caregiver decision/sick', 'Caregiver chose not to give the CTX/Placebo because baby was sick or for other reasons'),
    ('OTHER', 'Other'),
    ('N/A', 'Not Applicable'),
)

REASON_MISSED_PROPHYLAXIS = (
    ('caregiver forgot', 'Caregiver forgot to give the NVP'),
    ('caregiver ran out/lost', 'Caregiver ran out of NVP or lost the bottle'),
    ('caregiver away', 'Primary caregiver was away from home and did not have another person give the NVP'),
    ('infant away', 'Infant was away from home and the NVP bottle was not at the other location'),
    ('caregiver decision/sick', 'Caregiver chose not to give the NVP because baby was sick or for other reasons'),
    ('OTHER', 'Other'),
)

STUDY_STATUS = (
    ('followup', 'Lost can followup'),
    ('no followup', 'Lost no followup'),
    )

TIMES_BREASTFED = (
    ('<1 per week', '1. Less than once per week'),
    ('<1 per day, but at least once per week', '2. Less than once per day, but at least once per week'),
    ('about 1 per day on most days', '3. About once per day on most days'),
    ('>1 per day, but not for all feedings', '4. More than once per day, but not for all feedings'),
    ('For all feedings', '5. For all feedings (i.e no formula or other foods or liquids)'),
    ('N/A', 'Not Applicable'),
)

VACCINES = (
    ('HBV', 'HBV'),
    ('BCG', 'BCG'),
    ('DTap', 'DTap'),
    ('Hib', 'Hib'),
    ('Polio', 'Polio'),
    ('Pneumoccal_Vaccine', 'Pneumoccal Vaccine'),
    ('Rotavirus', 'Rotavirus'),
    ('MMR', 'MMR'),
    ('Varicella', 'Varicella'),
    ('Influenza', 'Influenza'),
    )

VISIT_INFO_SOURCE = [
    ('participant', '1. Clinic visit with participant'),
    ('other_contact', '2. Other contact with participant (for example telephone call)'),
    ('other_doctor', '3. Contact with external health care provider/medical doctor'),
    ('family', '4. Contact with family or designated person who can provide information'),
    ('chart', '5. Hospital chart or other medical record'),
    ('telephone', '6. Telephone call with participant'),
    ('OTHER', '9. Other'),
]

# DONT CHANGE THESE !!
VISIT_REASON = [
    ('scheduled', '1. Scheduled visit/contact'),
    ('missed', '2. Missed Scheduled visit'),
    ('unscheduled', '3. Unscheduled visit at which lab samples or data are being submitted'),
    ('lost', '4. Lost to follow-up (use only when taking subject off study)'),
    ('death', '5. Death'),
    ('off study', '6. Subject has completed the study'),
    ('deferred', '7. Deferred (2010 only)'),
    ('vital status', '8. Vital Status'),
]

WATER_USED = (
    ('Water direct from source', 'Water direct from source'),
    ('Water boiled immediately before use', 'Water boiled immediately before use'),
    ('Water boiled earlier and then stored', 'Water boiled earlier and then stored'),
    ('Specifically treated water', 'Specifically treated water'),
    ('OTHER', 'Other (specify)'),
    ('N/A', 'Not Applicable'),
)

ALIVE_DEAD_UNKNOWN = (
    ('ALIVE', 'Alive'),
    ('DEAD', 'Deceased'),
    ('UNKNOWN', 'Unknown'),
    )

STOOL_TEXTURE_DESC = (
    ('formed_with_blood', 'Formed without blood'),
    ('formed_without_blood', 'Formed with blood'),
    ('loose_without_blood', 'Loose but not watery and without blood'),
    ('loose_with_blood', 'Loose but not watery and with blood'),
    ('watery_without_blood', 'Watery without blood'),
    ('watery_with_blood', 'Watery with blood'),
    )

ILLNESS_CLASSIFICATION = (
    ('N/A', 'Not applicable'),
    ('respi_illness', 'Respiratory Illness'),
    ('gastro_illness', 'Gastrointestinal illness (examples including vomiting, diarrhea or both)'),
    ('OTHER', 'Other'),
    )

STOOLS_PAST_24HOURS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('>7', '>7'),
    ('UNKNOWN', 'Unknown')
    )

CONTINUOUS_LOOSE_STOOLS = (
    ('1day', '1 day'),
    ('2days', '2 days'),
    ('3days', '3 days'),
    ('4days', '4 days'),
    ('5days', '5 days'),
    ('6days', '6 days'),
    ('7days', '7 days'),
    ('>7days', 'Greater than 7 days but not more than 13 days'),
    ('>14days', '14 days or greater')
    )
