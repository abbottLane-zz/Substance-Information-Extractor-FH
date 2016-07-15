class PreDoc:
    def __init__(self, time, text, mrn):
        self.timestamp=time
        self.text=text
        self.mrn=mrn
        self.possible_ids = set()
        self.caisis_id = None