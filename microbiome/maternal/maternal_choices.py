from microbiome.constants import LIVE, STILL_BIRTH
from edc_constants.choices import YES, NO

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
    ('Poster/pamphlet at ANC', 'Recruitment poster/pamphlet at ANC'),
    ('ANC clinic staff', 'ANC clinic staff'),
    ('Staff at site of delivery', 'Staff at site of delivery'),
    ('BHP recruiter', 'BHP recruiter'),
    ('OTHER', 'Other, specify'),
)

RECRUIT_CLINIC = (
    ('PHH', 'Gaborone(PMH)'),
    ('SLH', 'Molepolole(SLH)'),
    ('ATHLONE', 'Lobatse(Athlone)'),
    ('G.West Clinic', 'G.West Clinic'),
    ('Old Naledi Clinic', 'Old Naledi Clinic'),
    ('BH3 Clinic', 'BH3 Clinic'),
    ('Mafitlhakgosi Clinic', 'Mafitlhakgosi Clinic'),
    ('Tsopeng Clinic', 'Tsopeng Clinic'),
    ('Peleng East Clinic', 'Peleng East Clinic'),
    ('Tlokweng main', 'Tlokweng Main Clinic'),
    ('Khayakhulu', 'Khayakhulu Clinic'),
    ('Nkoyaphiri', 'Nkoyaphiri Clinic'),
    ('Phuthadikobo', 'Phuthadikobo Clinic'),
    ('Boribamo', 'Boribamo Clinic'),
    ('Borakalalo', 'Borakalalo Clinic'),
    ('Bokaa', 'Bokaa Clinic'),
    ('Kgosing', 'Kgosing Clininc'),
    ('MCC', 'Molepolole Community Centre'),
    ('OTHER health facility', 'Other health facilities not associated with study site'),
    ('HOME', 'Home'),
    ('OTHER location', 'Other location'),
)

PRIOR_PREG_HAART_STATUS = (
    ('Received continuos HAART from the time she started',
     'Received continuos HAART from the time she started'),
    ('Had treatment interruption but restarted ',
     'Had treatment interruption but restarted HAART prior to this pregnancy'),
    ('interruption never restarted',
     'Had treatment interruption and never restarted HAART prior to this pregnancy'),
)

MARITAL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Cohabiting', 'Cohabiting'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    ('OTHER', 'Other, specify'),)

ETHNICITY = (
    ('Black African', 'Black African'),
    ('Caucasian', 'Caucasian'),
    ('Asian', 'Asian'),
    ('OTHER', 'Other, specify'),)

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
    ('OTHER', 'Other, specify'),)

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
    ('OTHER', 'Other, specify'),)

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
    ('OTHER', 'Other water source (stream, borehole, rainwater, etc)'),)

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
    ('OTHER', 'Other, specify'),)

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
