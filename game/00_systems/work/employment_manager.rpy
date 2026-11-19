# LOLA - Employment Manager
# Handles jobs, shifts, and work
# Ren'Py 8.6.0

init python:
    # ============================================================================
    # EMPLOYMENT SYSTEM
    # ============================================================================

    # Starter job definition (provisional - pending visual review)
    starter_job = {
        "id": "cafe_barista",
        "name": "Cafe Barista",
        "workplace": "The Daily Grind Cafe",
        "wage": 12,  # per hour
        "shift_length": 4,  # hours
        "energy_cost": 15,
        "description": "Serve coffee and customers at a local cafe.",
    }

    def get_job_info():
        """Get current job information."""
        if current_job:
            return current_job
        return None

    def start_job(job_definition):
        """Start a new job."""
        global employment_state, current_job, work_experience
        employment_state = "employed"
        current_job = job_definition
        work_experience += 1

    def end_job():
        """End current employment."""
        global employment_state, current_job
        employment_state = "unemployed"
        current_job = None

    def work_shift():
        """Complete a work shift."""
        global shift_today, money, energy, shifts_worked, workplace_hours

        if not current_job:
            return False

        job = current_job
        earnings = job["wage"] * job["shift_length"]

        # Pay the player
        add_money(earnings, "{} shift wages".format(job["name"]))

        # Apply energy cost
        energy = max(0, energy - job["energy_cost"])

        # Track stats
        shift_today = True
        shifts_worked += 1
        workplace_hours += job["shift_length"]

        return True

    def get_earnings():
        """Get how much a full shift earns."""
        if current_job:
            return current_job["wage"] * current_job["shift_length"]
        return 0

    def is_employed():
        """Check if currently employed."""
        return employment_state == "employed" and current_job is not None

    def get_workplace_name():
        """Get the name of current workplace."""
        if current_job:
            return current_job.get("workplace", "Work")
        return "Unemployed"

    def get_job_description():
        """Get job description."""
        if current_job:
            return current_job.get("description", "Working.")
        return "Not working."
