from bhp077.apps.microbiome.constants import LIVE, STILL_BIRTH
from edc_constants.choices import YES, NO
from edc_constants.constants import CONTINUOUS, RESTARTED, OTHER, STOPPED, NOT_APPLICABLE, NEW

LIVE_STILL_BIRTH = (
    (LIVE, 'live birth'),
    (STILL_BIRTH, 'still birth')
)

YES_NO_DNT_DWTA = (
    (YES, YES),
    (NO, NO),
    ('Dont know right now', 'I do not know right now'),
    ('DWTA', 'Don\'t want to answer'))

NEXT_CHILD_PLAN = (
    ('within 2years', 'Within the next 2 years'),
    ('between 2-5years from now', 'From 2 years to 5 years from now'),
    ('More than 5years from now', 'More than 5 years from now'),
    ('Dont know right now', 'I do not know right now'),
    ('DWTA', 'Don\'t want to answer'))

RECRUIT_SOURCE = (
    ('ANC clinic staff', 'ANC clinic staff'),
    ('Staff at site of delivery', 'Staff at site of delivery'),
    ('BHP recruiter/clinician', 'BHP recruiter/clinician'),
    (OTHER, 'Other, specify'),
)

RECRUIT_CLINIC = (
    ('PMH', 'Gaborone(PMH)'),
    ('G.West Clinic', 'G.West Clinic'),
    ('BH3 Clinic', 'BH3 Clinic'),
    ('Nkoyaphiri', 'Nkoyaphiri Clinic'),
    ('Lesirane', 'Lesirane Clinic'),
    (OTHER, 'Other health facilities not associated with study site'),
)

DELIVERY_HEALTH_FACILITY = (
    ('PMH', 'Gaborone(PMH)'),
    ('G.West Clinic', 'G.West Clinic'),
    ('BH3 Clinic', 'BH3 Clinic'),
    ('Lesirane', 'Lesirane Clinic'),
    (OTHER, 'Other health facilities not associated with study site'),
)

PRIOR_PREG_HAART_STATUS = (
    (CONTINUOUS,
     'Received continuous HAART from the time she started'),
    (RESTARTED,
     'Had treatment interruption but restarted HAART prior to this pregnancy'),
    (STOPPED,
     'Had treatment interruption and never restarted HAART prior to this pregnancy'),
)

MARITAL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Cohabiting', 'Cohabiting'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    (OTHER, 'Other, specify'),)

ETHNICITY = (
    ('Black African', 'Black African'),
    ('Caucasian', 'Caucasian'),
    ('Asian', 'Asian'),
    (OTHER, 'Other, specify'),)

HIGHEST_EDUCATION = (
    ('None', 'None'),
    ('Primary', 'Primary'),
    ('Junior Secondary', 'Junior Secondary'),
    ('Senior Secondary', 'Senior Secondary'),
    ('Tertiary', 'Tertiary'),)

CURRENT_OCCUPATION = (
    ('Housewife', 'Housewife'),
    ('Salaried (government)', 'Salaried (government)'),
    ('Salaried (private, not including domestic work)', 'Salaried (private, not including domestic work)'),
    ('Domestic work (paid)', 'Domestic work (paid)'),
    ('Self-employed', 'Self-employed'),
    ('Student', 'Student'),
    ('Unemployed', 'Unemployed'),
    (OTHER, 'Other, specify'),)

MONEY_PROVIDER = (
    ('You', 'You'),
    ('Partner/husband', 'Partner/husband'),
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Sister', 'Sister'),
    ('Brother', 'Brother'),
    ('Aunt', 'Aunt'),
    ('Uncle', 'Uncle'),
    ('Grandmother', 'Grandmother'),
    ('Grandfather', 'Grandfather'),
    ('Mother-in-law or Father-in-law', 'Mother-in-law or Father-in-law'),
    ('Friend', 'Friend'),
    ('Work collegues', 'Work collegues'),
    ('Unsure', 'Unsure'),
    (OTHER, 'Other, specify'),)

MONEY_EARNED = (
    ('None', 'None'),
    ('<P200 per month / <P47 per week', '<P200 per month / <P47 per week'),
    ('P200-500 per month / P47-116 per week', 'P200-500 per month / P47-116 per week'),
    ('P501-1000 per month / P117 - 231 per week', 'P501-1000 per month / P117 - 231 per week'),
    ('P1001-5000 per month / P212 - 1157 per week', 'P1001-5000 per month / P212 - 1157 per week'),
    ('P5000 per month / >P1157 per week', 'P5000 per month / >P1157 per week'),
    ('Unsure', 'Unsure'), )

WATER_SOURCE = (
    ('Piped directly into the house', 'Piped directly into the house'),
    ('Tap in the yard', 'Tap in the yard'),
    ('Communal standpipe', 'Communal standpipe'),
    (OTHER, 'Other water source (stream, borehole, rainwater, etc)'),)

COOKING_METHOD = (
    ('Gas or electric stove', 'Gas or electric stove'),
    ('Paraffin stove', 'Paraffin stove'),
    ('Wood-burning stove or open fire', 'Wood-burning stove or open fire'),
    ('No regular means of heating', 'No regular means of heating'),)

TOILET_FACILITY = (
    ('Indoor toilet', 'Indoor toilet'),
    ('Private latrine for your house/compound', 'Private latrine for your house/compound'),
    ('Shared latrine with other compounds', 'Shared latrine with other compounds'),
    ('No latrine facilities', 'No latrine facilities'),
    (OTHER, 'Other, specify'),)

HOUSE_TYPE = (
    ('Formal:Tin-roofed, concrete walls', 'Formal: Tin-roofed, concrete walls'),
    ('Informal: Mud-walled or thatched', 'Informal: Mud-walled or thatched'),
    ('Mixed formal/informal', 'Mixed formal/informal'),
    ('Shack/Mokhukhu', 'Shack/Mokhukhu'),)

KNOW_HIV_STATUS = (
    ('Nobody', 'Nobody'),
    ('1 person', '1 person'),
    ('2-5 people', '2-5 people'),
    ('6-10 people', '6-10 people'),
    ('More than 10 people', 'More than 10 people'),
    ('dont know', 'I do not know'),)

DX = (
    ('Pneumonia suspected, no CXR or microbiologic confirmation',
     'Pneumonia suspected, no CXR or microbiologic confirmation'),
    ('Pneumonia, CXR confirmed, no bacterial pathogen',
     'Pneumonia, CXR confirmed, no bacterial pathogen'),
    ('Pneumonia, CXR confirmed, bacterial pathogen isolated (specify pathogen)',
     'Pneumonia, CXR confirmed, bacterial pathogen isolated (specify pathogen)'),
    ('Pulmonary TB, suspected(no CXR or microbiologic confirmation)',
     'Pulmonary TB, suspected(no CXR or microbiologic confirmation)'),
    ('Pulmonary TB, CXR-confirmed (no microbiologic confirmation)',
     'Pulmonary TB, CXR-confirmed (no microbiologic confirmation)'),
    ('Pulmonary TB, smear and/or culture positive',
     'Pulmonary TB, smear and/or culture positive'),
    ('Extrapulmonary TB,suspected (no CXR or microbiologic confirmation) ',
     'Extrapulmonary TB,suspected (no CXR or microbiologic confirmation) '),
    ('Extrapulmonary TB, smear and/or culture positive',
     'Extrapulmonary TB, smear and/or culture positive'),
    (('Acute diarrheal illness (bloody diarrhean OR increase of at least 7 stools per day '
     'OR life threatening for less than 14 days) '),
     ('Acute diarrheal illness (bloody diarrhean OR increase of at least 7 stools per day OR '
      'life threatening for less than 14 days)')),
    ('Chronic diarrheal illness (as above but for 14 days or longer) ',
     'Chronic diarrheal illness (as above but for 14 days or longer) '),
    ('Acute Hepatitis in this pregnancy: Drug related ',
     'Acute Hepatitis in this pregnancy: Drug related '),
    ('Acute Hepatitis in this pregnancy:Traditional medication related',
     'Acute Hepatitis in this pregnancy:Traditional medication related'),
    ('Acute Hepatitis in this pregnancy:Fatty liver disease',
     'Acute Hepatitis in this pregnancy:Fatty liver disease'),
    ('Acute Hepatitis in this pregnancy:Hepatitis A', 'Acute Hepatitis in this pregnancy:Hepatitis A'),
    ('Acute Hepatitis in this pregnancy:Hepatitis B ', 'Acute Hepatitis in this pregnancy:Hepatitis B'),
    ('Acute Hepatitis in this pregnancy:Alcoholic', 'Acute Hepatitis in this pregnancy:Alcoholic'),
    ('Acute Hepatitis in this pregnancy:Other/Unkown', 'Acute Hepatitis in this pregnancy:Other/Unkown'),
    ('Sepsis, unspecified', 'Sepsis, unspecified'),
    ('Sepsis, pathogen specified', 'Sepsis, pathogen specified'),
    ('Meningitis, unspecified', 'Meningitis, unspecified'),
    ('Meningitis, pathogen specified', 'Meningitis, pathogen specified'),
    ('Appendicitis', 'Appendicitis'),
    ('Cholecystitis/cholanangitis', 'Cholecystitis/cholanangitis'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Acute Renal failure', 'Acute Renal failure (Record highest creatinine level if tested outside of the study)'),
    ('Anemia', 'Anemia (Only report grade 3 or 4 anemia based on the lab value drawn outside the study)'),
    ('Pregnancy/peripartum cardiomyopathy or CHF ', 'Pregnancy/peripartum cardiomyopathy or CHF '),
    ('Drug rash on HAART', 'Drug rash on HAART'),
    ('Trauma/Accident', 'Trauma/Accident'),
    ('Other serious (grade 3 or 4) infection, specify',
     'Other serious (grade 3 or 4) infection(not listed above), specify'),
    ('Other serious (grade 3 or 4) non-infectious diagnosis, specify',
     'Other serious (grade 3 or 4) non-infectious diagnosis(not listed above), specify'),
)

REASON_FOR_HAART = (
    ('maternal masa', '1. HAART for maternal treatment (qualifies by Botswana guidelines)'),
    ('pmtct bf', '2. HAART for PMTCT while breastfeeding'),
    ('pp arv tail', '3. Brief postpartum antiretroviral "tail"'),
    ('unsure', '4. Unsure'),
    (OTHER, '9. OTHER'),
    (NOT_APPLICABLE, 'Not applicable'))

# haart modification
ARV_DRUG_LIST = (
    ('Nevirapine', 'NVP'),
    ('Kaletra', 'KAL'),
    ('Aluvia', 'ALU'),
    ('Truvada', 'TRV'),
    ('Tenoforvir', 'TDF',),
    ('Zidovudine', 'AZT'),
    ('Lamivudine', '3TC'),
    ('Efavirenz', 'EFV'),
    ('Didanosine', 'DDI'),
    ('Stavudine', 'D4T'),
    ('Nelfinavir', 'NFV'),
    ('Abacavir', 'ABC'),
    ('Combivir', 'CBV'),
    ('Ritonavir', 'RTV'),
    ('Trizivir', 'TZV'),
    ('Raltegravir', 'RAL'),
    ('Saquinavir,soft gel capsule', 'FOR'),
    ('Saquinavir,hard capsule', 'INV'),
    ('Kaletra or Aluvia', 'KAL or ALU'),
    ('Atripla', 'ATR'),
    ('HAART,unknown', 'HAART,unknown'),
)

DOSE_STATUS = (
    (NEW, 'New'),
    ('Permanently discontinued', 'Permanently discontinued'),
    ('Temporarily held', 'Temporarily held'),
    ('Dose modified', 'Dose modified'),
    ('Resumed', 'Resumed'),
    ('Not initiated', 'Not initiated'),
)

ARV_MODIFICATION_REASON = (
    ('Initial dose', 'Initial dose'),
    ('Never started', 'Never started'),
    ('Toxicity decreased_resolved', 'Toxicity decreased/resolved'),
    ('Completed PMTCT intervention', 'Completed PMTCT intervention'),
    ('Completed postpartum tail', 'Completed postpartum "tail"'),
    ('Scheduled dose increase', 'Scheduled dose increase'),
    ('Confirmed infant HIV infection, ending study drug', 'Confirmed infant HIV infection, ending study drug'),
    ('completed protocol', 'Completion of protocol-required period of study treatment'),
    ('HAART not available', 'HAART not available'),
    ('Anemia', 'Anemia'),
    ('Bleeding', 'Bleeding'),
    ('CNS symptoms', 'CNS symptoms (sleep, psych, etc)'),
    ('Diarrhea', 'Diarrhea'),
    ('Fatigue', 'Fatigue'),
    ('Headache', 'Headache'),
    ('Hepatotoxicity', 'Hepatotoxicity'),
    ('Nausea', 'Nausea'),
    ('Neutropenia', 'Neutropenia'),
    ('Thrombocytopenia', 'Thrombocytopenia'),
    ('Vomiting', 'Vomiting'),
    ('Rash', 'Rash'),
    ('Rash resolved', 'Rash resolved'),
    ('Neuropathy', 'Neuropathy'),
    ('Hypersensitivity_allergic reaction', 'Hypersensitivity / allergic reaction'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Lactic Acidiosis', 'Lactic Acidiosis'),
    ('Pancytopenia', 'Pancytopenia'),
    ('Virologic failure', 'Virologic failure'),
    ('Immunologic failure', 'Immunologic failure(CD4)'),
    ('Clinical failure', 'Clinical failure'),
    ('Clinician request', 'Clinician request, other reason (including convenience)'),
    ('Subject request', 'Subject request, other reason (including convenience)'),
    ('Non-adherence with clinic visits', 'Non-adherence with clinic visits'),
    ('Non-adherence with ARVs', 'Non-adherence with ARVs'),
    ('Death', 'Death'),
    (OTHER, 'Other'),
)

REASON_UNSEEN_AT_CLINIC = (
    ('not_tried', 'I have not yet sought the clinic'),
    ('no_booking', 'I went to the clinic but could not get a booking'),
    ('in_confinement', 'I am observing confinement'),
    ('not_sexually_active', 'I am not sexually active right now'),
    ('no_contraception_bf', 'I do not need contraception because I am breastfeeding'),
    ('too_far', 'The clinic is too far from my home'),
    ('partner_refused', 'My partner does not want me to attend'),
    ('mother_refused', 'My mother does not want me to attend'),
    (OTHER, 'Other'),
)

REASON_CONTRACEPTIVE_NOT_INITIATED = (
    ('no_options', 'There was not an option I preferred'),
    ('no_stock_for_preference',
     'The option I preferred was out of stock (state option if this answer is indicated)'),
    ('not_sexually_active', 'I am not currently sexually active'),
    ('disrespected', 'I felt disrespected by the SRH clinic'),
    ('no_contraception_bf',
     'I was told that because I am breastfeeding, I do not need a contraceptive metod'),
    ('partner_refused',
     'My current partner does not want me to use a contraceptive method'),
    ('was not attended by a clinician', 'I was not attended by a clinician when I went to the SRH clinic'),
    (OTHER, 'Other'),
)

SITE = (
    ('Gaborone', 'Gaborone'),
)
