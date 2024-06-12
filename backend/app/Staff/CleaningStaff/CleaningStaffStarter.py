from app.Staff.CleaningStaff.CleaningStaff import CleaningStaff

def start_cleaning_staff(staff_id, name):
    cleaning_staff = CleaningStaff(staff_id, name)
    return cleaning_staff