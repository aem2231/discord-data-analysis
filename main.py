import os
from pathlib import Path
from generate_test_data import generate
from simple_term_menu import TerminalMenu # NOTE: Change to different library to support windows
from most_said_wordcloud import most_said_wordcloud

# basic menue to configure options
def main():
    use_test_data: bool = False
    use_blacklist: bool = False
    options: list[str] = ["Yes", "No"]

    test_data_menu = TerminalMenu(options, title="Use test data?")
    menu_entry_index: int = test_data_menu.show() # menu_entry_index is the choice made by the user.                                                   
    if menu_entry_index == 0:                     # for example, if they chose "Yes", menu entry index will equal 0
        use_test_data = True
        if os.path.exists("test_data"): 
            overwite_test_data_menu = TerminalMenu(options, title="A test data directory already exists. \nWould you like to generate new data?")
            menu_entry_index = overwite_test_data_menu.show()
            if menu_entry_index == 0:
                generate() 
                os.system('cls' if os.name == 'nt' else 'clear')
        else:
            generate()
            os.system('cls' if os.name == 'nt' else 'clear')

    blacklist_menu = TerminalMenu(options, title="Use blacklist?")
    menu_entry_index: int = blacklist_menu.show()
    if menu_entry_index == 0:
        use_blacklist = True
        print("Blackist will be used.\n")

    
    most_said_wordcloud(use_blacklist, use_test_data)
        
if __name__ == "__main__":
    main()