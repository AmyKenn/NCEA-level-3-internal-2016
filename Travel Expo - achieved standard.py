#Amy Kennard
#AS91637

from tkinter import *

#Suporting class to keep track of traveller's details
class TravelInfo:
    def __init__(self, name, age, number, trips, local):
        self.name = name
        self.age = age
        self.number = number
        self.trips = trips
        self.local = local

class TravelExpoGUI:
    def __init__(self, parent):
        self.traveller_objects = [] #list to append every traveller's information
        
        #Costs of trips as constant variables
        ZEALANDIA_COST = 10 #$
        TE_PAPA_COST = 15 #$
        CABLE_CAR_COST = 12.50 #$

        #setting up the frames
        self.collect_data_frame = Frame(parent) #collecting data frame
        self.collect_data_frame.grid(row = 1, column = 0, sticky = W)
        permanent_frame = Frame(parent) #permanent frame
        permanent_frame.grid(row = 2, columnspan = 2)
        self.display_data_frame = Frame(parent) #display of the data frame
        self.display_data_frame.grid(row = 1, column = 0, columnspan = 2)
        logo_frame = Frame(parent)
        logo_frame.grid(row = 0, column = 0, sticky = W)
        self.display_screen_frame = Frame(parent)
        self.display_screen_frame.grid(row = 0, column = 1)
        self.summary_frame = Frame(parent)
        self.summary_frame.grid(row = 1, columnspan = 2)

        #setting up logo for logo_frame
        self.logo_img = PhotoImage(file = "travelexpo.gif") #importing the logo
        self.new_logo_img = self.logo_img.subsample(2,2) #resizes the logo by using "subsample"
        self.logo_label = Label(logo_frame, image = self.new_logo_img)
        self.logo_label.grid(sticky = W) #don't need to grid as nothing else is being put the the logo_frame

        #setting up widgets for display_screen_frame
        self.screen_label = Label(self.display_screen_frame)
        self.screen_label.configure(text = "COLLECTING PERSON DATA")
        self.screen_label.grid(row = 0, column = 1, sticky = S)
        
        self.show_btn = Button(self.display_screen_frame)
        self.show_btn.configure(text = "SHOW ALL", command = self.show_display_screen)
        self.show_btn.grid(row = 1, column = 1, sticky = N)
        
        #setting up the labels for collect_data_frame
        self.enter_label = Label(self.collect_data_frame, text = "Please enter the following:")
        self.enter_label.grid(row = 0, column = 0, sticky = W)
        self.name_label = Label(self.collect_data_frame, text = "Name:")
        self.name_label.grid(row = 1, column = 0, sticky = W)
        self.age_label = Label(self.collect_data_frame, text = "Age:")
        self.age_label.grid(row = 2, column = 0, sticky = W)
        self.number_label = Label(self.collect_data_frame, text = "Cell Number:")
        self.number_label.grid(row = 3, column = 0, sticky = W)
        self.trip_attend_label = Label(self.collect_data_frame, text = "Please select the trip(s) you wish to attend:")
        self.trip_attend_label.grid(row = 4, column = 0, sticky = W)
        self.wellington_label = Label(self.collect_data_frame, text = "Please select whether or not you are a resident of Wellington:")
        self.wellington_label.grid(row = 8, column = 0)
        self.error_label = Label(self.collect_data_frame, text = "")
        self.error_label.grid(row = 11, column = 0)

        #setting up the entrys for collect_data_frame
        self.name_entry = Entry(self.collect_data_frame)
        self.name_entry.grid(row = 1, column = 0, sticky = E)
        self.age_entry = Entry(self.collect_data_frame)
        self.age_entry.grid(row = 2, column = 0, sticky = E)
        self.number_entry = Entry(self.collect_data_frame)
        self.number_entry.grid(row = 3, column = 0, sticky = E)

        #setting up the button for collect_data_frame
        self.enter_btn = Button(self.collect_data_frame, text = "ENTER", command = self.collect_user_details)
        self.enter_btn.grid(row = 12, column = 0)

        #setting up the checkbuttons for collect_data_frame
        self.cb_trips = ["Zealandia", "Te Papa", "CableCar with morning tea"]
        self.travel_trips = [] #empty list to append each trip to
        #sets up each check button for each trip
        for i in range(len(self.cb_trips)):
            self.trip_option = StringVar()
            self.trip_option.set("0") #so that no checkbutton is selected
            self.travel_trips.append(Checkbutton(self.collect_data_frame, variable = self.trip_option, onvalue = self.cb_trips[i], offvalue= "0",text = self.cb_trips[i]))
            self.travel_trips[i].var = self.trip_option
        self.travel_trips[0].grid(row = 5, column = 0, sticky = W, padx = 20) #sticky so that they line up
        self.travel_trips[1].grid(row = 6, column = 0, sticky = W, padx = 20)
        self.travel_trips[2].grid(row = 7, column = 0, sticky = W, padx = 20)

        #setting up radiobutton for collect_data_frame
        self.wellington_option = StringVar()
        self.wellington_option.set(" ")
        self.wellington_resident = Radiobutton(self.collect_data_frame, text = "Wellington Resident", value = "Wellington Resident", variable = self.wellington_option)
        self.wellington_resident.grid(row = 9, column = 0, sticky = W, padx = 20)
        self.not_wellington_resident = Radiobutton(self.collect_data_frame, text = "Outside Wellington", value = "Outside Wellington", variable = self.wellington_option)
        self.not_wellington_resident.grid(row = 10, column = 0, sticky = W, padx = 20)

        #setting up widgets for permanent frame
        self.resident_option = StringVar() #StringVar for searching resident options
        self.resident_option.set(" ") #so that no radiobutton is selected
        self.search_label = Label(permanent_frame, text = "SEARCH FOR NAMES OF THOSE:")
        self.search_label.grid(row = 0, columnspan = 2)
        self.in_wellington_rb = Radiobutton(permanent_frame, text = "Wellington Resident", value = "Wellington Resident", variable = self.resident_option, command = self.in_summary)
        self.in_wellington_rb.grid(row = 1, column = 0)
        self.out_wellington_rb = Radiobutton(permanent_frame, text = "Outside Wellington", value = "Outside Wellington", variable = self.resident_option, command = self.out_summary)
        self.out_wellington_rb.grid(row = 1, column = 1)

        self.count = 0 #to keep track of travellers when viewing display screen
        self.position = 0 #need this for screen 3!
        tripstring = ""

        #setting up the traveller_info_label
        self.traveller_info_label = Label(self.display_data_frame, text = "")
        self.traveller_info_label.grid(row = 0, columnspan = 2)

    def display_info_label(self):
        #crafting the trip string for "traveller_info_label", depending on how many trips the traveller selected
        for i in range(len(self.traveller_objects)):
            tripstring = "" #resets trips
            if len(self.traveller_objects[self.count].trips) == 1: #if traveller selected 1 trip
                tripstring = ' '.join(self.traveller_objects[self.count].trips)
            elif len(self.traveller_objects[self.count].trips) == 2: #if traveller selected 2 trips
                tripstring = ' and '.join(self.traveller_objects[self.count].trips)
            elif len(self.traveller_objects[self.count].trips) == 3: #if traveller selected 3 trips
                tripstring = ((self.traveller_objects[self.count].trips[0]) + ", " + (self.traveller_objects[self.count].trips[1]) + ", and " + (self.traveller_objects[self.count].trips[2]))
        print(tripstring)

        self.traveller_info_label.configure(text = ( (self.traveller_objects[self.count].name) + " is joining trips for " + tripstring))

    def show_display_screen(self):
        #removes unwanted frames and buttons
        self.collect_data_frame.grid_remove()
        self.summary_frame.grid_remove()
        self.display_data_frame.grid() #displays the "display" frame
        self.show_btn.grid_remove() #hides unwanted button

        #setting up widgets for display_data_frame
        #setting up label widgets
        self.screen_label.configure(text = "DISPLAYING PERSON DATA")
        self.display_info_label() #calls the "display_info_label" function

        #setting up button widgets
        self.new_btn = Button(self.display_screen_frame, text = "ADD NEW PERSON", command = self.show_collect_screen)
        self.new_btn.grid(row = 1, column = 1)
        if len(self.traveller_objects) > 1:
            self.prev_btn = Button(self.display_data_frame, text = "PREVIOUS", state = NORMAL, command = self.previous_traveller)
        if self.count == 0:
            self.prev_btn = Button(self.display_data_frame, text = "PREVIOUS", state = DISABLED, command = self.previous_traveller)
        self.prev_btn.grid(row = 1, column = 0, sticky = W)
        
        if len(self.traveller_objects) == 1: #so that the "next" button knows to start off disabled if only one traveller's data has been collected
            self.next_btn = Button(self.display_data_frame, text = "NEXT", state = DISABLED, command = self.next_traveller)
        elif len(self.traveller_objects) != 1:
            self.next_btn = Button(self.display_data_frame, text = "NEXT", state = NORMAL, command = self.next_traveller)
        self.next_btn.grid(row = 1, column = 1, sticky = E)

    def next_traveller(self):
        self.count += 1
        if self.count != 0:
            self.prev_btn.configure(state = NORMAL)
        if self.count == len(self.traveller_objects) - 1: #end of list
            self.next_btn.configure(state = DISABLED)
        elif self.count >= len(self.traveller_objects):
            self.count = 0

        self.display_info_label() #calls the "display_info_label" function
        

    def previous_traveller(self):
        self.count -= 1
        if self.count == 0:
            self.prev_btn.configure(state = DISABLED)
        if self.count != len(self.traveller_objects):
            self.next_btn.configure(state = NORMAL)
        elif self.count < 0:
            self.count = len(self.traveller_objects) - 1

        self.display_info_label() #calls the "display_info_label" function

    def show_collect_screen(self):
        #hides the unwanted frames
        self.summary_frame.grid_remove()
        self.display_data_frame.grid_remove() 
        self.collect_data_frame.grid() #shows wanted frame
        self.new_btn.grid_remove() #hides unwanted button
        self.show_btn.configure(text = "SHOW ALL")
        self.show_btn.grid(row = 1, column = 1, sticky = N) #showing wanted button,
        #griding again to keep in place.
        self.screen_label.configure(text = "COLLECTING PERSON DATA")
        self.traveller_info_label.configure(text = "")

    def in_summary(self):
        self.show_summary_screen() #runs the function
        self.resident_label = Label(self.summary_frame, text = "Names of those in Wellington:") 
        self.resident_label.grid(row = 0, column = 0, sticky = W)
        
        for i in range(len(self.traveller_objects)):
            self.name_label = Label(self.summary_frame, text = self.traveller_objects[i].name)
            self.name_label.grid(row = 2 + i, column = 0, sticky = W)
            self.number_label = Label(self.summary_frame, text = self.traveller_objects[i].number)
            self.number_label.grid(row = 2 + i, column = 1)
            self.position += 1
            
        self.total_zealandia_label = Label(self.summary_frame, text = "Total number for Zealandia: ") #will add total later
        self.total_zealandia_label.grid(row = 3 + self.position, columnspan = 3)
        self.total_tepapa_label = Label(self.summary_frame, text = "Total number for Te Papa: ") #will add total later
        self.total_tepapa_label.grid(row = 4 + self.position, columnspan = 3)
        self.total_cablecar_label = Label(self.summary_frame, text = "Total number for Cable Car: ") #will add total later
        self.total_cablecar_label.grid(row = 5 + self.position, columnspan = 3)

    def out_summary(self):
        self.show_summary_screen() #runs the function
        self.resident_label = Label(self.summary_frame, text = "Names of those out of Wellington:") 
        self.resident_label.grid(row = 0, column = 0, sticky = W)
        
        for i in range(len(self.traveller_objects)):
            self.name_label = Label(self.summary_frame, text = self.traveller_objects[i].name)
            self.name_label.grid(row = 2 + i, column = 0, sticky = W)
            self.number_label = Label(self.summary_frame, text = self.traveller_objects[i].number)
            self.number_label.grid(row = 2 + i, column = 1)
            self.position += 1
            
        self.total_zealandia_label = Label(self.summary_frame, text = "Total number for Zealandia: ") #will add total later
        self.total_zealandia_label.grid(row = 3 + self.position, columnspan = 3)
        self.total_tepapa_label = Label(self.summary_frame, text = "Total number for Te Papa: ") #will add total later
        self.total_tepapa_label.grid(row = 4 + self.position, columnspan = 3)
        self.total_cablecar_label = Label(self.summary_frame, text = "Total number for Cable Car: ") #will add total later
        self.total_cablecar_label.grid(row = 5 + self.position, columnspan = 3)
        
    def show_summary_screen(self):
        #removing frame and showing frame
        self.display_data_frame.grid_remove()
        self.collect_data_frame.grid_remove()
        self.summary_frame.grid()

        #setting up widgets for summary_frame
        #label widgets
        self.screen_label.configure(text = "SUMMARY OF TRIPS")
        self.screen_label.grid(columnspan = 2)
        
        self.summary_name_label = Label(self.summary_frame, text = "Name:")
        self.summary_name_label.grid(row = 1, column = 0, sticky = W)
        self.summary_number_label = Label(self.summary_frame, text = "Cell Phone:")
        self.summary_number_label.grid(row = 1, column = 1)
        self.summary_price_label = Label(self.summary_frame, text = "Amount to Pay:")
        self.summary_price_label.grid(row = 1, column = 2, sticky = E)
        
        self.price_label = Label(self.summary_frame, text = "") #will add prices later
        self.price_label.grid(row = 2, column = 2)
        
        #making button widgets visible
        self.new_btn = Button(self.display_screen_frame, text = "ADD NEW PERSON", command = self.show_collect_screen) #setting it up again in case user clicks a radiobutton first
        self.new_btn.grid(row = 1, column = 1)
        self.show_btn.grid(row = 1, column = 2)
        
    def collect_user_details(self):
        #stores the user's information
        self.user_name = self.name_entry.get() #stores traveller's name
        self.user_age = int(self.age_entry.get()) #stores traveller's age
        self.user_number = self.number_entry.get() #stores traveller's cell number
        self.user_resident = self.wellington_option.get() #stores traveller's resident option

        self.user_trips = [] #new list to append the user's selected trips to

        #stores the traveller's destinations
        for i in range(len(self.travel_trips)):
            if self.travel_trips[i].var.get()!= "0": #if a checkbutton box does not equal unticked (if it has been ticked)
                 self.user_trips.append(self.travel_trips[i].var.get())
        print(self.user_trips)

        #error testing for user's age
        if self.user_age < 16: #is the user's age is less than 16
            self.error_label.configure(text = "Traveller must be 16 years or older", fg = "red") #text colour is red
        elif self.user_age > 99:
            self.error_label.configure(text = "Please enter sensible age", fg = "red")
        else:
            self.error_label.configure(text = "") #clears the error label 
            #appends the user's information to a sublist in the list "traveller_objects"
            self.traveller_objects.append(TravelInfo(self.user_name, self.user_age, self.user_number, self.user_trips, self.user_resident))
        
        #emptying the entry widgets so the user can enter another traveller's details
        self.name_entry.delete(0, 'end') 
        self.age_entry.delete(0, 'end')
        self.number_entry.delete(0, 'end')

        #resetting the radiobutton widgets so the user can select another traveller's resident option
        self.wellington_option.set(" ") 
        
        #resetting the checkbutton widgets so the user can tick another traveller's destinations
        for i in range(len(self.travel_trips)):
            self.travel_trips[i].deselect()
             
#main routine
if __name__=="__main__":
    root = Tk()
    root.title("Travel Expo")
    travelexpo = TravelExpoGUI(root)
    root.geometry("550x500+400+100")
    root.mainloop()
