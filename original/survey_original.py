print(" ==== (F1) FORMULA 1 SURVEY ====")  # Title for Survey (I chose to an F1 Survey since it's my passion)

Correct_Class = "11SEG261"  # The Correct_Class variable holds the value for the correct class password for students to gain access to the quiz.

choice_1 = "Continue" # The choice_1 variable was created to display an option for the user to continue with the survey.
choice_2 = "Quit" # The choice_2 variable was created to display an option for the user to leave the survey, if they don't want to continue.
choice_3 = "Restart" # The choice_3 variable was created to display an option for the user to restart the survey, if they want to re enter the quiz.

survey_data = [                                                                                                                                                     
    ["1. How much knowledge do you hold about F1?", "(A) Zero", "(B) Little", "(C) Some", "(D) A lot"],                                                                  
    ["2. How long have you watched F1?", "(A) Between 0-1 Years", "(B) Between 1-3 Years", "(C) Between 3-5 Years", "(D) More than 5 years"],                  
    ["3. How many full seasons have you watched in F1?", "(A) None", "(B) 1", "(C) 2-3", "(D) Greater than 3"],                                                        
    ["4. What high performing team would you go for?", "(A) McLaren", "(B) Ferrari", "(C) Mercedes", "(D) Red Bull"],
    ["5. What middle performing team would you go for?", "(A) Williams", "(B) Haas", "(C) Aston Martin", "(D) Alpine"],
    ["6. Where would you go and watch an F1 race?", "(A) Asia/Southeast Asia", "(B) Europe", "(C) South America", "(D) Middle East"],
    ["7. Through philosophy, which team do you think will dominate in the future?", "(A) Red Bull", "(B) Mercedes", "(C) Ferrari", "(D) Audi"],
    ["8. Which legendary F1 driver would you pick to race with?", "(A) Ayrton Senna", "(B) Michael Schumacher", "(C) Nigel Mansell", "(D) Damon Hill"],      
    ["9. If you had to drive for an F1 Team, what would it be?", "(A) Mercedes", "(B) Williams", "(C) Ferrari", "(D) McLaren"],
    ["10. Do you show interest in F1?", "(A) Yes (Rarely)", "(B) Yes (Somewhat)", "(C) Yes (Fully)", "(D) Never"]                                                
]                                                                                                                                                                     

# --- Get user details first ---
user_name = input("Enter your name: ") # The user_name variable displays an input to the user to enter their name. 
user_class = input("Enter your class: ") # The user_class variable displays an input to the user to enter the correct class code.

''' This if and else condition checks if the user_class input matches the correct variable for the Correct_class variable. If user_class isn't equal to the variable in Correct_class, it prints (Sorry. Access Denied. The correct code is 11SEG261.)'''
if user_class != Correct_Class:
    print("Sorry. Access Denied. The correct code is '11SEG261'. ")        
else: 
    running = True # The running variable operates the code and invites the users into the survey.

    while running: #The while loop allows the survey to run and allows the user to either: Continue, Quit or Restart.
        print(f"\nWelcome {user_name} from {user_class}") # The f'string was used to combine strings with a variable to welcome the user to the survey.
        print("Please choose an option:") # The user is welcomed to choose an option to continue in the survey.
        print("1.", choice_1) # The first option is printed and is called within the choice_1 variable.x
        print("2.", choice_2) # The second option is printed and is called within the choice_2 variable.
        print("3.", choice_3) # The third option is printed and is called within the choice_3 variable.

        user_choice = input("Enter your choice (1/2/3): ") # The user_choice variable provides an input for the users to enter their choice through an integer and whether to choose in continuing with the quiz.

        if user_choice == "1":  # If the user chooses to type in 1, the survey continues.
            print("\nGood luck with the survey!" + "You chose the option " + choice_1) # A message appears and wishes the user the best of luck with their survey.
            answers = [] # The answers varaible is stored in an empty list. Their answers are stored in the answers list.

            for item in survey_data: # The items are the list of the indexes of the questions that are in the survey_data variable. 
                print("\n" + item[0]) # This command prints the first line of questions and the remaining answers in every breaking line.
                for option in item[1:]:  # This command prints the remaining questions and answers from the survey_run list. This finishes off an entire survey.
                    print(option) # The print command, prints every questions and answer options.

                ans_choice = input("What's your answer? (A/B/C/D): ").upper() # The ans_choice variable is an input that asks the user to enter their answers to each question through an upper case format. The upper() format makes the inputs as captial.
               
                while ans_choice not in ["A", "B", "C", "D"]:  # This while loop operator checks if the user enters their answer option through the four letters 'A,B,C,D' in caps.
                    print("Invalid answer. Please enter A, B, C, or D.") # The survey doesn't accept any other answer apart from the four caps letters. If the user types in anything else, the survey won't accept the answer and ask the user to re enter their answer.
                    ans_choice = input("What's your answer? (A/B/C/D): ").upper() # It repeats the input function and indicates the user to resubmit their answer in an upper case format.

                print("Answer Successfully Submitted!") # If the user successfully submits their answer options to any of these letters, the survey prints this message.
                answers.append(ans_choice) # The append() function allows the answers to be stored in the answers[] list.

            # --- Displays final survey results ---
            print("\n" + "_" * 20) # This print command creates a space between the lines. The integer indicated displays the number of spaces used to display the heading. The /n operator creates a space between the lines.
            print("FINAL SURVEY RESULTS") # On the next line, this print command displays the title of the survey results.
            print("=" * 30) # On the next line, this print command prints the equal sign 30 times to provide space between the title.

            for index in range(len(answers)): # The index operator identifies the position of the position of each answer in the answers[] list. The len function calculates the total number of answers in the answers[] list, as shown with the range operator, setting the range of the count.
                question_text = survey_data[index][0].upper() # The question_text variable prints the questions of the survey_data list through the index and 0 operator. The .upper() operator prints the questions and answers in upper cased format.
                user_ans = answers[index].upper() # The user_ans variable prints the answers to the respective questions. This is displayed with the .upper() format.
                print(f"{question_text}\nYOUR ANSWER: {user_ans}\n") # This print command displays the organisation of the questions and answers. The /n function creates a break between the lines.

            confirm = input("Are you happy with your answers? Please say (Y/N): ").upper() # In the end, the confirm variable asks the user if they're happy with their answers. Where the user needs to operate through an upper case operator.

            while confirm not in ["Y", "N"]: # This while loop checks if the user has entered either Y or N for their choice.
             print("Unapplicable answer. Please enter Y or N.") # It follows with a message that reminds the user to reselect their choice.
             confirm = input("Are you happy with your answers? (Y/N): ").upper() # Returns the confirm input.  


            if confirm == "Y": # If the confirm variable is Y, then the survey closes.
                print("Thank you for your time! Your Survey has been submitted.") # It prints a message thanking the user for their time in completing the survey.
                running = False  # The running operator is False thus it doesn't operate.
            else:
                print("Ok. Let's return and do the survey again!") # If the confirm variable is N, the survey starts from the beginning and prints a motivated message for the user to resubmit their answers.
                

        elif user_choice == "2":  # The user can now choose to leave the survey if they wish to.
           
            print("See you next time!")  # If they choose to, then the survey prints a goodbye message and the running operator closes, ultimately closing the survey.
            running = False

        elif user_choice == "3": # The user can also choose to re enter the first beginning of the survey, where they re enter their credentials and restart the survey.
        
            print("Rebooting the survey menu...")  # Prints a message indicating the user that the survey is re opening.
           

        else:
            print("Invalid choice. Please enter 1, 2, or 3.") # If the choice doesn't correspond to any of the three options, the survey prints a message telling the user to renter the choices integer.

            

   

    




























