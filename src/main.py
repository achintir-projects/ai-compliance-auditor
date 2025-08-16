from context import ContextCapture
from standards import StandardsParser
from evidence import EvidenceIntake
from analysis import GapAnalysis
from reporting import ReportGenerator, RemediationPlanner
from monitoring import MonitoringSetup
import json

def main(jurisdiction):
    """
    Main entry point for the AI Compliance Auditor application.
    """
    print("Starting AI Compliance Auditor...")
    
    # Step 1: Context & Scope Capture
    context_capturer = ContextCapture()
    audit_context = context_capturer.gather_context(jurisdiction)
    
    print("\nAudit context successfully captured.")
    
    # Step 2: Standards Retrieval & Parsing
    standards_parser = StandardsParser(
        global_standards_path='data/global_standards.json',
        local_laws_path='data/local_banking_laws.json'
    )
    parsed_standards = standards_parser.retrieve_and_parse(audit_context['jurisdiction'])
    
    print("\nParsed Standards:")
    print(json.dumps(parsed_standards, indent=2))

    # Step 3: Evidence & Data Intake
    evidence_intake = EvidenceIntake(parsed_standards)
    
    # Generate a complete questionnaire from all standards and laws
    declarative_evidence = {}
    if 'global' in parsed_standards:
        for std_name, std_data in parsed_standards['global'].items():
            if 'clauses' in std_data and std_data['clauses']:
                declarative_evidence[std_name] = {clause: "yes" for clause in std_data['clauses']}

    if 'local' in parsed_standards:
        for jurisdiction, laws in parsed_standards['local'].items():
            for law_name, law_data in laws.items():
                if 'clauses' in law_data and law_data['clauses']:
                    declarative_evidence[law_name] = {clause: "yes" for clause in law_data['clauses']}
    
    evidence_record = evidence_intake.process_declarative_evidence(declarative_evidence)
    
    print("\nCollected Evidence Record:")
    print(json.dumps(evidence_record, indent=2))

    # Step 4: Gap Analysis
    gap_analyzer = GapAnalysis(parsed_standards, evidence_record)
    gap_analysis_results = gap_analyzer.analyze()
    
    print("\nGap Analysis Results:")
    print(json.dumps(gap_analysis_results, indent=2))

    # Step 5: Audit Report Generation
    report_generator = ReportGenerator(audit_context, gap_analysis_results)
    audit_report = report_generator.generate_report()
    
    print("\n--- Audit Report ---")
    print(audit_report)

    # Step 6: Remediation Playbook
    remediation_planner = RemediationPlanner(gap_analysis_results)
    remediation_playbook = remediation_planner.create_playbook()
    
    print("\n--- Remediation Playbook ---")
    print(remediation_playbook)

    # Step 7: Continuous Monitoring Setup
    monitoring_setup = MonitoringSetup(gap_analysis_results)
    monitoring_checklist = monitoring_setup.generate_checklist()
    
    print("\n--- Continuous Monitoring Checklist ---")
    print(monitoring_checklist)


if __name__ == "__main__":
    jurisdiction_to_audit = "UAE, UK, USA, EU, Ghana, Nigeria and Pakistan"
    main(jurisdiction_to_audit)
