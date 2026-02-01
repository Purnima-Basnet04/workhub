from datetime import date

def calculate_total_experience(experiences):
    total_days = 0

    for exp in experiences:
        start = exp.start_date
        end = exp.end_date or date.today()
        total_days += (end - start).days

    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30

    return {
        "years": years,
        "months": months,
        "days": days,
    }
