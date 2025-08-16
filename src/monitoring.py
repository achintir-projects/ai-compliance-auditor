class MonitoringSetup:
    """
    Handles Step 7: Continuous Monitoring Setup.
    """
    def __init__(self, gap_analysis_results):
        self.gap_analysis_results = gap_analysis_results

    def generate_checklist(self):
        """
        Generates a recurring checklist for periodic verification of key controls.
        """
        print("\n--- Step 7: Continuous Monitoring Setup ---")
        
        checklist = []
        checklist.append("="*150)
        checklist.append("CONTINUOUS MONITORING CHECKLIST")
        checklist.append("="*150)
        
        compliant_controls = [result for result in self.gap_analysis_results if result['status'] == 'Compliant']
        
        if not compliant_controls:
            checklist.append("\nNo compliant controls found to monitor.")
            return "\n".join(checklist)

        checklist.append(f"\n{'Control':<50} | {'Check Description':<50} | {'Evidence Type':<25} | {'Due Date'}")
        checklist.append("---" * 50)

        for control in compliant_controls:
            checklist.append(f"{control['control']:<50} | {'Verify that evidence is still current and valid.':<50} | {'Declarative':<25} | {'Quarterly'}")
        
        checklist.append("---" * 50)
            
        print("Successfully generated continuous monitoring checklist.")
        return "\n".join(checklist)
