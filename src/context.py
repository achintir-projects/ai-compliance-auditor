class ContextCapture:
    """
    Handles Step 1: Context & Scope Capture.
    """
    def __init__(self):
        self.context = {}

    def gather_context(self, jurisdiction):
        """
        Gathers information from the user to define the audit scope.
        """
        print("--- Step 1: Context & Scope Capture ---")
        self.context['industry'] = 'banking' # Defaulting to banking as per spec
        print("Industry: banking (default)")
        
        self.context['jurisdiction'] = jurisdiction
        
        # Placeholders for other questions from the spec
        self.context['entity_details'] = {}
        self.context['regulations_in_scope'] = []
        
        print("\nContext Captured:")
        print(f"- Jurisdiction: {self.context['jurisdiction']}")
        
        return self.context
