from dataparser_v1.modules.parser_main import DataParser
from dataparser_v1.modules.input_window import InputWindow
from dataparser_v1.modules.file_splitter import FileFinder
from dataparser_v1.modules.final_path_finder import PathFinder
from dataparser_v1.modules.plate_id_generator import PlateIDGenerator
from dataparser_v1.modules.display_window import DisplayData
from dataparser_v1.modules.archive_proj_data import ArchiveData
from tkinter import messagebox, Tk


def main():
    InputWindow()
    # Add break from run
    msg = Tk()
    msg.withdraw()
    go_next = messagebox.askyesno(
        title="Wait",
        message="Do you want to continue? Data will be lost if canceled."
    )
    msg.destroy()
    if go_next:
        FileFinder()
        PlateIDGenerator()
        PathFinder()
        msg = Tk()
        msg.withdraw()
        go_next = messagebox.askyesno(
            title="Wait",
            message="Do you want to continue? Data will be lost if canceled."
        )
        msg.destroy()
        if go_next:
            DisplayData()
            ArchiveData()

            msg = Tk()
            msg.withdraw()
            parse_data = messagebox.askyesno(
                title="Continue?",
                message="Would you like to run the data parser?"
            )
            msg.destroy()
            if parse_data:
                DataParser()
                window = Tk()
                window.withdraw()
                messagebox.showinfo("Way to go!", "Data has been output!")
                window.destroy()


# TODO 1 add the ability to quit process at any time

# TODO 2 add ability to go back  to previous screen in case data was not added


if __name__ == "__main__":
    main()
