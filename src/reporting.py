class ReportGenerator:
    """
    Handles Step 5: Audit Report Generation.
    """
    def __init__(self, audit_context, analysis_results):
        self.audit_context = audit_context
        self.analysis_results = analysis_results

    def generate_report(self):
        """
        Generates the final audit report.
        """
        print("\n--- Step 5: Audit Report Generation ---")
        
        report = []
        report.append("="*80)
        report.append("AI COMPLIANCE AUDIT REPORT")
        report.append("="*80)
        
        # Executive Summary
        report.append("\n## 1. Executive Summary")
        report.append("This report details the findings of an automated compliance audit...")
        
        # Scope and Methodology
        report.append("\n## 2. Scope & Methodology")
        report.append(f"Industry: {self.audit_context.get('industry')}")
        report.append(f"Jurisdictions: {self.audit_context.get('jurisdiction')}")
        
        # Detailed Gap Table
        report.append("\n## 3. Detailed Gap Table")
        report.append("-" * 80)
        report.append(f"{ 'Standard':<20} | { 'Control':<50} | { 'Status':<25} | {'Rationale'}")
        report.append("-" * 80)
        for result in self.analysis_results:
            report.append(f"{result['standard']:<20} | {result['control']:<50} | {result['status']:<25} | {result['rationale']}")
        report.append("-" * 80)
        
        print("Successfully generated audit report.")
        return "\n".join(report)

class RemediationPlanner:
    """
    Handles Step 6: Remediation Playbook.
    """
    def __init__(self, analysis_results):
        self.analysis_results = analysis_results

    def create_playbook(self):
        """
        Creates a remediation plan for identified gaps.
        """
        print("\n--- Step 6: Remediation Playbook ---")
        
        playbook = []
        playbook.append("="*80)
        playbook.append("REMEDIATION PLAYBOOK")
        playbook.append("="*80)
        
        gaps = [result for result in self.analysis_results if result['status'] != 'Compliant']
        
        if not gaps:
            playbook.append("\nNo gaps found. No remediation actions required.")
            return "\n".join(playbook)

        for gap in gaps:
            playbook.append(f"\n## Gap: {gap['control']} ({gap['standard']})")
            playbook.append(f"Status: {gap['status']}")
            playbook.append(f"Rationale: {gap['rationale']}")
            
            playbook.append("\n### Remediation Plan:")
            playbook.append(f"- **Objective:** Achieve compliance for control '{gap['control']}'.")
            playbook.append(f"- **Tasks:**")
            if gap['status'] == 'Evidence Not Provided':
                playbook.append("  - 1. Identify and locate relevant evidence for this control.")
                playbook.append("  - 2. Upload evidence to the compliance management system.")
                playbook.append("  - 3. Request a re-evaluation of the control.")
            elif gap['status'] == 'Non-Compliant':
                playbook.append("  - 1. Analyze the root cause of the non-compliance.")
                playbook.append("  - 2. Develop and implement a corrective action plan.")
                playbook.append("  - 3. Monitor the effectiveness of the corrective action.")

            playbook.append(f"- **Responsible Role:** Compliance Officer")
            playbook.append(f"- **Estimated Timeline:** 2 weeks")
            playbook.append(f"- **Resources Needed:** Access to relevant documentation and systems.")
            playbook.append("-" * 80)
            
        print("Successfully generated remediation playbook.")
        return "\n".join(playbook)
