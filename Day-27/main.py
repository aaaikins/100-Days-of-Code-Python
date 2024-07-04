import tkinter as tk

# Creates new tkinter window
window = tk.Tk()
window.title("Mile to Km converter")
window.config(padx= 20, pady= 20)


def miles_to_km():
    '''
    converts miles to km
    '''
    miles = float(miles_input.get())
    km = 1.609 * miles
    km_value_label.config(text= str(km))


# Creates Entry instance to take input for miles
miles_input = tk.Entry(width=10)
miles_input.grid(column=1,row=0)

# Creates label for 'miles'
miles_label = tk.Label(text= "Miles", font= ("Arial", 15))
miles_label.grid(column=2, row=0)

# Creates label for 'is equal to'
is_equal_to_label = tk.Label(text= "is equal to", font= ("Arial", 15))
is_equal_to_label.grid(column=0, row=1)

# Creates label to hold the value in kilometers
km_value_label = tk.Label(text= "0", font= ("Arial", 15))
km_value_label.grid(column=1, row=1)

# Creates label for 'km'
km_label= tk.Label(text= "Km", font= ("Arial", 15))
km_label.grid(column=2, row=1)

# Creates a button for 'calculate'
calculate_button = tk.Button(text= "Calculate", command= miles_to_km)
calculate_button.grid(column=1, row=2)


window.mainloop()