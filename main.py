import pyinputplus as pyip
from extraction import extraction_process
from mapping import mapping_process
from reports import report_process
from calculations import calculation_process

processes = {'extraction': extraction_process,
             'mapping': mapping_process,
             'calculation': calculation_process,
             'report': report_process
             }


class Dialog:

    def __init__(self, process_dict: dict):
        self.voice = 'Programme started'
        self.user_choice: str | int | None = None
        self.process_dict = processes
        self.response = None
        self.user_accept = True

    def choose_process(self):
        self.voice = 'Choose one of processes below'
        print(self.voice)
        print('--------------')
        print('Processes: ')
        print('--------------')

        # Choose option
        for i in enumerate(self.process_dict):
            print(i[0] + 1, ' - ', i[1], sep='')

        process_number = pyip.inputNum(prompt='Process: ',
                                       min=1,
                                       max=len(self.process_dict)
                                       )

        self.user_choice = list(self.process_dict)[process_number - 1]
        print(self.user_choice)

        return self

    def run_process(self):
        self.process_dict[self.user_choice]()
        self.voice = 'Do you want to continue?'
        return self

    def user_accept_processing(self):
        choice = pyip.inputYesNo(prompt='(y/n) - ',
                                 yesVal='y',
                                 noVal='n')
        self.user_accept = True if choice == 'y' else False
        return self.user_accept

    def run(self):
        print(self.voice)
        while self.user_accept:
            self.choose_process()
            self.run_process()
            print(self.voice)
            self.user_accept = self.user_accept_processing()


if __name__ == '__main__':
    Dialog(processes).run()
    print()
    # add code processing
