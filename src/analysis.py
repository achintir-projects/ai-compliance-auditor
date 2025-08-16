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

        # Iterate through all controls in parsed_standards
        for std_type, standards in self.parsed_standards.items():
            for std_name, std_data in standards.items():
                if 'clauses' in std_data and std_data['clauses']:
                    for control_info in std_data['clauses']:
                        control_name = control_info['name'] if isinstance(control_info, dict) else control_info
                        control_type = control_info.get('type', 'secondary') if isinstance(control_info, dict) else 'secondary'

                        evidence = self.evidence_record.get(std_name, {}).get(control_name)

                        status = "Evidence Not Provided"
                        rationale = f"Evidence for this control was not collected."

                        if evidence:
                            if evidence.lower() == 'yes':
                                status = "Compliant"
                                rationale = f"Evidence for '{control_name}' was provided."
                            else:
                                status = "Non-Compliant"
                                rationale = f"Evidence for '{control_name}' was not provided or was negative."
                                if control_type == 'key':
                                    rationale += " (Major Breach: This is a key control)."
                        
                        self.gap_analysis_results.append({
                            "standard": std_name,
                            "control": control_name,
                            "status": status,
                            "rationale": rationale,
                            "type": control_type
                        })
                        print(f"Analyzed '{control_name}': {status}")

        return self.gap_analysis_results