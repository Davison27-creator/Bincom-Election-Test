class PollingUnit:
    def __init__(self, id, name, lga):
        self.id = id
        self.name = name
        self.lga = lga

class PartyResult:
    def __init__(self, id, polling_unit_id, party_name, votes):
        self.id = id
        self.polling_unit_id = polling_unit_id
        self.party_name = party_name
        self.votes = votes