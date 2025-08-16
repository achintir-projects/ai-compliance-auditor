class EvidenceIntake:
    """
    Handles Step 3: Evidence & Data Intake.
    """
    def __init__(self, parsed_standards):
        self.parsed_standards = parsed_standards
        self.evidence_record = {}

    def process_declarative_evidence(self, evidence_data):
        """
        Processes declarative (yes/no) evidence provided by the user.
        """
        print("\n--- Step 3: Evidence & Data Intake ---")
        
        for standard, controls in evidence_data.items():
            for control, evidence in controls.items():
                if standard not in self.evidence_record:
                    self.evidence_record[standard] = {}
                self.evidence_record[standard][control] = evidence
                print(f"Recorded evidence for '{control}' in '{standard}': {evidence}")

        return self.evidence_record
