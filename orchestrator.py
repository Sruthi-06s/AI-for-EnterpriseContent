import time
from datetime import datetime
from utils import log_audit, calculate_time_saved

class ContentOrchestrator:
    """Enhanced workflow manager with human-in-the-loop"""
    
    def __init__(self, drafting_agent, compliance_agent, 
                 localization_agent, distribution_agent, intelligence_agent):
        self.drafting = drafting_agent
        self.compliance = compliance_agent
        self.localization = localization_agent
        self.distribution = distribution_agent
        self.intelligence = intelligence_agent
        self.audit_log = []
        self.pending_approval = None
        self.approval_status = None
    
    def run_workflow(self, brief, regions=["US"], channels=["LinkedIn"], 
                     human_approved=None, human_feedback=None):
        """Execute the full content pipeline with human approval gate"""
        
        start_time = time.time()
        
        try:
            # Stage 1: Draft
            self._log("draft", "started", brief)
            draft = self.drafting.execute(brief)
            self._log("draft", "completed", {"word_count": len(draft.get('draft', ''))})
            
            # Stage 2: Compliance Check
            self._log("compliance", "started", {})
            compliance = self.compliance.execute(draft)
            self._log("compliance", "completed", {"score": compliance.get('score', 0)})
            
            # Stage 3: HUMAN-IN-THE-LOOP GATE
            # If compliance is not approved OR if we're waiting for human input
            if compliance.get('status') != "approved":
                self._log("human_review", "needed", {
                    "score": compliance.get('score', 0),
                    "issues": compliance.get('issues', []),
                    "message": compliance.get('message', '')
                })
                
                # Check if human has provided approval
                if human_approved is None:
                    # First time - return pending state
                    self.pending_approval = {
                        "draft": draft,
                        "compliance": compliance,
                        "brief": brief,
                        "regions": regions,
                        "channels": channels
                    }
                    return {
                        "status": "pending_human_approval",
                        "draft": draft,
                        "compliance": compliance,
                        "pending_review": True,
                        "audit_log": self.audit_log
                    }
                elif human_approved:
                    # Human approved - continue workflow
                    self._log("human_review", "approved", {"feedback": human_feedback or "No feedback"})
                else:
                    # Human rejected with feedback
                    self._log("human_review", "rejected", {"feedback": human_feedback})
                    
                    # If feedback provided, update draft
                    if human_feedback:
                        self._log("draft", "revision_requested", {"feedback": human_feedback})
                        # Update brief with feedback for revision
                        revised_brief = brief.copy()
                        revised_brief["revision_feedback"] = human_feedback
                        draft = self.drafting.execute(revised_brief)
                        self._log("draft", "revised", {"word_count": len(draft.get('draft', ''))})
                        
                        # Re-run compliance on revised draft
                        compliance = self.compliance.execute(draft)
                        self._log("compliance", "recheck", {"score": compliance.get('score', 0)})
                        
                        # If still not approved, return to human again
                        if compliance.get('status') != "approved":
                            self.pending_approval = {
                                "draft": draft,
                                "compliance": compliance,
                                "brief": revised_brief,
                                "regions": regions,
                                "channels": channels
                            }
                            return {
                                "status": "pending_human_approval",
                                "draft": draft,
                                "compliance": compliance,
                                "pending_review": True,
                                "audit_log": self.audit_log
                            }
            
            # Stage 4: Localization (only if approved)
            self._log("localization", "started", {"regions": regions})
            localized = self.localization.execute(draft, regions)
            self._log("localization", "completed", {"versions": len(localized.get('versions', {}))})
            
            # Stage 5: Distribution
            self._log("distribution", "started", {"channels": channels})
            distribution = self.distribution.execute(draft, channels)
            self._log("distribution", "completed", {"published": len(distribution.get('published', []))})
            
            # Stage 6: Intelligence
            self._log("intelligence", "started", {})
            insights = self.intelligence.execute("content_123")
            self._log("intelligence", "completed", {"insights": insights.get('insights', [])[:2]})
            
        except Exception as e:
            self._log("error", "workflow_failed", {"error": str(e)})
            return {
                "status": "error",
                "error": str(e),
                "draft": {"draft": f"Error: {str(e)}", "status": "error"},
                "compliance": {"status": "error", "score": 0},
                "localized": {"versions": {}},
                "distribution": {"published": [], "failed": []},
                "insights": {"analysis": "Error occurred", "insights": [], "recommendations": []},
                "total_time_minutes": 0,
                "impact": calculate_time_saved(4.5, 0),
                "audit_log": self.audit_log
            }
        
        end_time = time.time()
        total_minutes = (end_time - start_time) / 60
        
        # Calculate impact
        impact = calculate_time_saved(4.5, total_minutes)
        
        return {
            "status": "completed",
            "draft": draft,
            "compliance": compliance,
            "localized": localized,
            "distribution": distribution,
            "insights": insights,
            "total_time_minutes": total_minutes,
            "impact": impact,
            "audit_log": self.audit_log
        }
    
    def _log(self, stage, action, details):
        try:
            entry = log_audit(stage, action, details)
            self.audit_log.append(entry)
        except Exception as e:
            print(f"Error in logging: {e}")