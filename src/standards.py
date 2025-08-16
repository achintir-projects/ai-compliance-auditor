import json

class StandardsParser:
    """
    Handles Step 2: Standards Retrieval & Parsing.
    """
    def __init__(self, global_standards_path, local_laws_path):
        with open(global_standards_path, 'r') as f:
            self.global_standards = json.load(f)
        with open(local_laws_path, 'r') as f:
            self.local_laws = json.load(f)
        self.parsed_standards = {}

    def retrieve_and_parse(self, jurisdictions):
        """
        Retrieves and parses standards from the database based on jurisdictions.
        """
        print("\n--- Step 2: Standards Retrieval & Parsing ---")
        
        # For simplicity, we'll treat the jurisdiction string as a list
        jurisdiction_list = [j.strip() for j in jurisdictions.replace(' and ', ',').split(',')]
        
        # Add all global standards
        self.parsed_standards['global'] = self.global_standards
        print("Retrieved global standards: " + ", ".join(self.global_standards.keys()))

        # Add local laws for the specified jurisdictions
        self.parsed_standards['local'] = {}
        for jur in jurisdiction_list:
            if jur in self.local_laws:
                self.parsed_standards['local'][jur] = self.local_laws[jur]
                print(f"Retrieved local laws for {jur}: " + ", ".join(self.local_laws[jur].keys()))

        return self.parsed_standards
