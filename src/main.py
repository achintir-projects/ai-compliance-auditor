from flask import Flask, request
from context import ContextCapture
from standards import StandardsParser
from evidence import EvidenceIntake
from analysis import GapAnalysis
from reporting import ReportGenerator, RemediationPlanner
from monitoring import MonitoringSetup
import json
import os

app = Flask(__name__)

def run_audit(jurisdiction):
    """
    Main entry point for the AI Compliance Auditor application.
    """
    # Construct absolute paths to data files
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    global_standards_path = os.path.join(project_root, 'data', 'global_standards.json')
    local_laws_path = os.path.join(project_root, 'data', 'local_banking_laws.json')

    # Step 1: Context & Scope Capture
    context_capturer = ContextCapture()
    audit_context = context_capturer.gather_context(jurisdiction)

    # Step 2: Standards Retrieval & Parsing
    standards_parser = StandardsParser(
        global_standards_path=global_standards_path,
        local_laws_path=local_laws_path
    )
    parsed_standards = standards_parser.retrieve_and_parse(audit_context['jurisdiction'])

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

    # Step 4: Gap Analysis
    gap_analyzer = GapAnalysis(parsed_standards, evidence_record)
    gap_analysis_results = gap_analyzer.analyze()

    # Step 5: Audit Report Generation
    report_generator = ReportGenerator(audit_context, gap_analysis_results)
    audit_report = report_generator.generate_report()

    # Step 6: Remediation Playbook
    remediation_planner = RemediationPlanner(gap_analysis_results)
    remediation_playbook = remediation_planner.create_playbook()

    # Step 7: Continuous Monitoring Setup
    monitoring__setup = MonitoringSetup(gap_analysis_results)
    monitoring_checklist = monitoring_setup.generate_checklist()
    
    # Combine all reports into a single HTML string
    html_output = "<h1>AI Compliance Auditor Report</h1>"
    html_output += "<h2>Audit Report</h2>"
    html_output += f"<pre>{audit_report}</pre>"
    html_output += "<h2>Remediation Playbook</h2>"
    html_output += f"<pre>{remediation_playbook}</pre>"
    html_output += "<h2>Continuous Monitoring Checklist</h2>"
    html_output += f"<pre>{monitoring_checklist}</pre>"
    
    return html_output

@app.route('/')
def index():
    jurisdiction_to_audit = request.args.get('jurisdiction', 'UAE, UK, USA, EU, Ghana, Nigeria and Pakistan')
    return run_audit(jurisdiction_to_audit)

if __name__ == '__main__':
    app.run(debug=True)
