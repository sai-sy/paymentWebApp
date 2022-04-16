from website.helper_functions import load_sheet

def spreadsheet_import_test():
    filename = 'import_saihaan_payments_2022-04-16.xlsx'
    import_type = 'Shifts'
    load_sheet.test_start(filename, import_type)

def main():
    spreadsheet_import_test()

if __name__ == '__main__':
    main()