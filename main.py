import os
from pathlib import Path
from modules.generate_test_data import generate
from modules.most_said_wordcloud import most_said_wordcloud
from modules.messages_by_year import messages_by_year
from modules.messages_by_month import messages_by_month
from modules.monthly_messages_by_year import monthly_messages_by_year
from pymenu import select_menu
import time

# Entry point for the program
# Uses pymenu to create simple menus
# Asks the user what they want to do, then calls relevent functions

def test_data_menu(options: list[str]) -> bool:
    use_test_data: bool = False
    test_data_option = select_menu.create_select_menu(options, "Use test data?")
    if test_data_option == "Yes":
        use_test_data = True
        if os.path.exists("test_data"):
            overwite_test_data_option = select_menu.create_select_menu(options, "You have existing test data.\nWould you like to overwrite it?")
            if overwite_test_data_option == "Yes":
                generate()
                os.system('cls' if os.name == 'nt' else 'clear')
        elif not os.path.exists("test_data"):
            generate()
            os.system('cls' if os.name == 'nt' else 'clear')
    return use_test_data

def blacklist_menu(options: list[str]) -> bool:
    blacklist_option = select_menu.create_select_menu(options, "Use blacklist?")
    if blacklist_option == "Yes":
        print("Blacklist will be used.")
        return True
    else:
        print("Blacklist will not be used.")
        return False
    
def choose_tool(tool_options: list[str]):
    tool_option = select_menu.create_select_menu(tool_options, "Pick a tool")
    return tool_options.index(tool_option)

def main():
    use_test_data: bool = False
    use_blacklist: bool = False
    options: list[str] = ["Yes", "No"]
    tool_options: list[str] = ["Messages by year", "Messages by month", "Monthly messages by year", "Most said wordcloud", "Quit"]
    tool_option: str = ""

    while tool_option != tool_options.index("Quit"):
        try: 
            tool_option = choose_tool(tool_options)
            if tool_option == 0:
                use_test_data = test_data_menu(options)
                messages_by_year(use_test_data)
            elif tool_option == 1:
                use_test_data = test_data_menu(options)
                messages_by_month(use_test_data)
            elif tool_option == 2:
                use_test_data = test_data_menu(options)
                monthly_messages_by_year(use_test_data)
            elif tool_option == 3:
                use_test_data = test_data_menu(options)
                use_blacklist = blacklist_menu(options)
                most_said_wordcloud(use_blacklist, use_test_data)
            elif tool_option == 4:
                break
        except IndexError as e:
            print(f"Choice out of range:\n{e}")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')





if __name__ == "__main__":
    main()