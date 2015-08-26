from getresults_identifier import AlphanumericIdentifier


class MaternalIdentifier(AlphanumericIdentifier):

    name = 'maternalidentifier'
    alpha_pattern = r'^[A-Z]{3}$'
    numeric_pattern = r'^[0-9]{4}$'
    seed = ['AAA', '0000']
