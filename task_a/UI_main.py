# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:31:42 2026

@author: lenno
"""

def Read_me(input_file:str = None) -> str:
    
    # Otherwise, show a menu
    print("Select simulation duration:")
    print("1: Example ")
    print("2: input file")
    
    
    choice = input("select option: ")
    if choice == '1':
        return "2,4,3,1,3"
    elif choice == '2':
        input_file = input("Enter input file: ")
        try:
            with open(input_file, "r") as f:
                #print(f.read().strip())
                clean_content = " ".join(line for line in f)
                clean = clean_content.replace(" ", "")
                return clean
        except FileNotFoundError:
            print(f" File '{input_file}' not found. Using example data.")
            return "2,4,3,1,3"
        
    else:
        # Fallback to the example if no file is provided
        return "2,4,3,1,3"
   
    


def default(days: int = None) -> int:
    User_choice = {"Choice_1": 80, "Choice_2": 256}
    # If a value was provided, just return it
    if days is not None:
        return int(days)
    
    # Otherwise, show a menu
    print("Select simulation duration:")
    print("1: 80 days")
    print("2: 256 days")
    print("3: Custom days")
    
    choice = input("Enter choice (1| 2 | 3): ")
    
    if choice == '1':
        return User_choice["Choice_1"]
    elif choice == '2':
        return User_choice["Choice_2"]
    elif choice == '3':
        custom_choice = input("Enter amount of days: ")
        return int(custom_choice)
    else:
        print("Invalid choice, defaulting to 80.")
        return 80