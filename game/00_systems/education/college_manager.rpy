# LOLA - College Manager
# Handles education, classes, and assignments
# Ren'Py 8.6.0

init python:
    # ============================================================================
    # EDUCATION SYSTEM
    # ============================================================================

    def get_education_progress():
        """Get current education progress."""
        return education_progress

    def add_education_progress(amount):
        """Add education progress."""
        global education_progress
        education_progress = min(100, education_progress + amount)
        gain = max(0, amount) // 5
        change_stat("learning", gain)
        if gain > 0:
            change_stat("intelligence", gain)

    def attend_class():
        """Attend a class session."""
        global classes_attended, education_progress
        classes_attended += 1
        education_progress = min(100, education_progress + 10)
        change_stat("energy", -15)
        change_stat("learning", 2)
        change_stat("intelligence", 2)

    def study_at_library(hours=1):
        """Study at the library."""
        global education_progress, library_visits
        library_visits += 1
        education_progress = min(100, education_progress + hours * 5)
        change_stat("energy", -hours * 5)
        change_stat("learning", max(0, hours))
        change_stat("intelligence", max(0, hours))

    def complete_assignment(assignment_name):
        """Complete an assignment."""
        global assignments_due, education_progress
        for item in list(assignments_due):
            name = item.get("name") if isinstance(item, dict) else item
            if name == assignment_name:
                assignments_due.remove(item)
                education_progress = min(100, education_progress + 20)
                change_stat("learning", 4)
                change_stat("intelligence", 4)
                return True
        return False

    def add_assignment(name, due_day=None):
        """Add an assignment due."""
        assignments_due.append({
            "name": name,
            "due_day": due_day,
        })

    def get_upcoming_assignments():
        """Get list of assignments due soon."""
        return assignments_due

    def has_completed_enough_credits():
        """Check if enough education progress for milestones."""
        return education_progress >= 50
