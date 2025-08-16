from flask import Flask, request, render_template
from context import ContextCapture
from standards import StandardsParser
from evidence import EvidenceIntake
from analysis import GapAnalysis
from reporting import ReportGenerator, RemediationPlanner
from monitoring import MonitoringSetup
import json
import os

app = Flask(__name__)

def get_project_home():
    """Gets the project home directory from the environment variable."""
    project_home = os.environ.get('PROJECT_HOME')
    if not project_home:
        # For local testing, set a default project_home
        project_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return project_home

@app.route('/')
def index():
    """Displays the questionnaire."""
    project_home = get_project_home()
    jurisdiction_to_audit = request.args.get('jurisdiction', 'UAE, UK, USA, EU, Ghana, Nigeria and Pakistan')
    
    # Construct absolute paths to data files
    global_standards_path = os.path.join(project_home, 'data', 'global_standards.json')
    local_laws_path = os.path.join(project_home, 'data', 'local_banking_laws.json')

    # Step 1: Context & Scope Capture
    context_capturer = ContextCapture()
    audit_context = context_capturer.gather_context(jurisdiction_to_audit)

    # Step 2: Standards Retrieval & Parsing
    standards_parser = StandardsParser(
        global_standards_path=global_standards_path,
        local_laws_path=local_laws_path
    )
    parsed_standards = standards_parser.retrieve_and_parse(audit_context['jurisdiction'])

    questions = {}
    if 'global' in parsed_standards:
        for std_name, std_data in parsed_standards['global'].items():
            if 'clauses' in std_data and std_data['clauses']:
                questions[std_name] = std_data['clauses']

    if 'local' in parsed_standards:
        for jurisdiction, laws in parsed_standards['local'].items():
            for law_name, law_data in laws.items():
                if 'clauses' in law_data and law_data['clauses']:
                    questions[law_name] = law_data['clauses']

    return render_template('questionnaire.html', questions=questions)

@app.route('/report', methods=['POST'])
def report():
    """Processes the questionnaire and displays the report."""
    project_home = get_project_home()
    jurisdiction_to_audit = request.args.get('jurisdiction', 'UAE, UK, USA, EU, Ghana, Nigeria and Pakistan')
    
    # Process the form data to get the evidence
    declarative_evidence = {}
    for key, value in request.form.items():
        standard, control = key.split('|')
        if standard not in declarative_evidence:
            declarative_evidence[standard] = {}
        declarative_evidence[standard][control] = value

    # Run the audit with the collected evidence
    audit_report, remediation_playbook, monitoring_checklist = run_audit(jurisdiction_to_audit, project_home, declarative_evidence)

    return render_template('report.html', audit_report=audit_report, remediation_playbook=remediation_playbook, monitoring_checklist=monitoring_checklist)


def run_audit(jurisdiction, project_home, declarative_evidence):
    """
    Main entry point for the AI Compliance Auditor application.
    """
    # Construct absolute paths to data files
    global_standards_path = os.path.join(project_home, 'data', 'global_standards.json')
    local_laws_path = os.path.join(project_home, 'data', 'local_banking_laws.json')

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
    monitoring_setup = MonitoringSetup(gap_analysis_results)
    monitoring_checklist = monitoring_setup.generate_checklist()
    
    return audit_report, remediation_playbook, monitoring_checklist

if __name__ == '__main__':
    os.environ['PROJECT_HOME'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.run(debug=True)
