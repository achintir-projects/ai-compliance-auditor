class GapAnalysis:
    """
    Handles Step 4: Gap Analysis.
    """
    def __init__(self, parsed_standards, evidence_record):
        self.parsed_standards = parsed_standards
        self.evidence_record = evidence_record
        self.gap_analysis_results = []

    def analyze(self):
        """
        Compares evidence against standards to find gaps.
        """
        print("\n--- Step 4: Gap Analysis ---")

        # This is a simplified analysis for the demo.
        # A full implementation would iterate through all controls in self.parsed_standards.

        # Analyze the evidence we have collected
        for standard, controls in self.evidence_record.items():
            for control, evidence in controls.items():
                if evidence.lower() == 'yes':
                    status = "Compliant"
                    rationale = f"Evidence for '{control}' was provided."
                else:
                    status = "Non-Compliant"
                    rationale = f"Evidence for '{control}' was not provided or was negative."
                
                self.gap_analysis_results.append({
                    "standard": standard,
                    "control": control,
                    "status": status,
                    "rationale": rationale
                })
                print(f"Analyzed '{control}': {status}")

        

        return self.gap_analysis_results
