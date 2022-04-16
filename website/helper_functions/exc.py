class SpreadSheetParseError(Exception):
    def __init__(self, error_note):
        self.error_note = error_note