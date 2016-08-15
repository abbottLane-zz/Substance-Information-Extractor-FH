import shelve


shelf_file = 'shelf.db'
PATIENTS = 'Patients'


def shelve_patients(patients):
    s = shelve.open(shelf_file)
    try:
        s[PATIENTS] = patients
    finally:
        s.close()


def unshelve_patients():
    s = shelve.open(shelf_file)
    try:
        patients = s[PATIENTS]
    finally:
        s.close()

    return patients
