from plugin import plugin
import csv


@plugin("note")
def write_agenda(ausis, s):
    exit = True
    csv_columns = ['Title', 'Description']
    mydict = {}

    while(exit):
        event_title = ausis.input("Write down the event title: ")
        event_description = ausis.input("Write down the event description: ")
        event_option = ausis.input("Anything more?(y/n): ")
        mydict[event_title] = event_description

        if(event_option == 'n'):
            exit = False

    if bool(mydict):
        print('New inputs are: ' + str(mydict))
        try:
            with open('agenda.csv', 'w') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in mydict.items():
                    writer.writerow([key, value])
        except IOError:
            print("I/O error")
    else:
        print('Nothing for the agenda')


@plugin("read agenda")
def read_agenda(ausis, s):
    try:
        f = open('agenda.csv', 'r')
        reader = csv.reader(f)
        for row in reader:
            print(row)
        f.close()
    except BaseException:
        print('There is not an agenda')
