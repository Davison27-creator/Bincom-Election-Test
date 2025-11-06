from models import PollingUnit, PartyResult

class ElectionDB:
    def __init__(self):
        self.polling_units = []
        self.party_results = []
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        # Create sample polling units
        units_data = [
            (1, "Polling Unit 1 - School", "LGA A"),
            (2, "Polling Unit 2 - Town Hall", "LGA A"), 
            (3, "Polling Unit 3 - Market Square", "LGA B"),
            (4, "Polling Unit 4 - Community Center", "LGA C"),
            (5, "Polling Unit 5 - Primary School", "LGA B"),
            (6, "Polling Unit 6 - Church Hall", "LGA C"),
            (7, "Polling Unit 7 - Mosque Annex", "LGA A"),
            (8, "Polling Unit 8 - Village Square", "LGA D")
        ]
        
        for unit_data in units_data:
            self.polling_units.append(PollingUnit(*unit_data))
        
        # Create sample party results
        results_data = [
            (1, 1, "PDP", 50), (2, 1, "APC", 45), (3, 1, "LP", 30), (4, 1, "NNPP", 15),
            (5, 2, "PDP", 60), (6, 2, "APC", 55), (7, 2, "LP", 25), (8, 2, "NNPP", 20),
            (9, 3, "PDP", 40), (10, 3, "APC", 65), (11, 3, "LP", 35), (12, 3, "NNPP", 10),
            (13, 4, "PDP", 70), (14, 4, "APC", 40), (15, 4, "LP", 45), (16, 4, "NNPP", 25),
            (17, 5, "PDP", 45), (18, 5, "APC", 75), (19, 5, "LP", 30), (20, 5, "NNPP", 15),
            (21, 6, "PDP", 80), (22, 6, "APC", 35), (23, 6, "LP", 40), (24, 6, "NNPP", 20),
            (25, 7, "PDP", 55), (26, 7, "APC", 60), (27, 7, "LP", 25), (28, 7, "NNPP", 10),
            (29, 8, "PDP", 65), (30, 8, "APC", 50), (31, 8, "LP", 35), (32, 8, "NNPP", 20)
        ]
        
        for result_data in results_data:
            self.party_results.append(PartyResult(*result_data))
    
    def get_all_polling_units(self):
        return self.polling_units
    
    def get_polling_unit_by_id(self, unit_id):
        for unit in self.polling_units:
            if unit.id == unit_id:
                return unit
        return None
    
    def get_results_by_polling_unit(self, unit_id):
        return [result for result in self.party_results if result.polling_unit_id == unit_id]
    
    def get_all_lgas(self):
        return sorted(list(set(unit.lga for unit in self.polling_units)))
    
    def get_results_by_lga(self, lga_name):
        lga_units = [unit.id for unit in self.polling_units if unit.lga == lga_name]
        return [result for result in self.party_results if result.polling_unit_id in lga_units]
    
    def add_new_result(self, polling_unit_id, party_name, votes):
        new_id = max([r.id for r in self.party_results]) + 1 if self.party_results else 1
        new_result = PartyResult(new_id, polling_unit_id, party_name, votes)
        self.party_results.append(new_result)
        return new_result
    
    def get_party_totals_by_lga(self, lga_name):
        results = self.get_results_by_lga(lga_name)
        party_totals = {}
        
        for result in results:
            if result.party_name in party_totals:
                party_totals[result.party_name] += result.votes
            else:
                party_totals[result.party_name] = result.votes
        
        return party_totals