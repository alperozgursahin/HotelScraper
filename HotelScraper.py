from datetime import datetime
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import csv
from tkcalendar import Calendar
from tkinter import messagebox 

class HotelScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Scraper App")
        self.large_font = ("Helvetica", 13, "bold")
        bg_color = "#F2F2F2"

        # City Selection
        self.city_label = ttk.Label(root, text="Select City",font = self.large_font)
        self.city_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.city_label.configure(background=bg_color)

        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(root, textvariable=self.city_var)
        self.city_combobox['values'] = ['Roma', "Stockholm","Venice","Warsaw","Helsinki","Amsterdam","Vilnius","Paris","Fulda","Liverpool","Berlin", "Seoul", "Frankfurt", "Kyoto"]  # These area for cities
        self.city_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        current_date = datetime.now()
        # Check-in Date
        self.checkin_label = ttk.Label(root, text="Check-in Date",font = self.large_font)
        self.checkin_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.checkin_label.configure(background=bg_color)

        self.checkin_calendar = Calendar(root, selectmode="day", year=current_date.year, month=current_date.month, day=current_date.day)
        self.checkin_calendar.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Check-out Date
        self.checkout_label = ttk.Label(root, text="Check-out Date",font = self.large_font)
        self.checkout_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.checkout_label.configure(background=bg_color)

        self.checkout_calendar = Calendar(root, selectmode="day", year=current_date.year, month=current_date.month, day=current_date.day)
        self.checkout_calendar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Currency Selection
        self.currency_label = ttk.Label(root, text="Currency",font = self.large_font)
        self.currency_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.currency_label.configure(background=bg_color)

        self.currency_var = tk.StringVar(value="Euro")
        self.currency_combobox = ttk.Combobox(root, textvariable=self.currency_var)
        self.currency_combobox['values'] = ["TL", "Euro"]
        self.currency_combobox.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        # Sort by Selection
        self.sort_by_label = ttk.Label(root, text="Sort by",font = self.large_font)
        self.sort_by_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.sort_by_label.configure(background=bg_color)

        self.sort_by_var = tk.StringVar(value="Review Score")
        self.sort_by_combobox = ttk.Combobox(root, textvariable=self.sort_by_var)
        self.sort_by_combobox['values'] = ["Review Score", "Secondary Review Score"]
        self.sort_by_combobox.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        # How much hotels selection
        self.top_label = ttk.Label(root, text="Top",font = self.large_font)
        self.top_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.top_label.configure(background=bg_color)

        self.top_var = tk.IntVar(value=5)
        self.top_combobox = ttk.Combobox(root, textvariable=self.top_var)
        self.top_combobox['values'] = [5, 10, 15, 20]
        self.top_combobox.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

        # Search Button
        self.search_button = ttk.Button(root, text="Search", command=self.search_hotels)
        self.search_button.grid(row=6, columnspan=2, padx=10, pady=10)
        self.search_button.configure(style='LightButton.TButton')

        # Text Box
        self.text_box = tk.Text(root, height=35, width=90, font=("Helvetica", 14))
        self.text_box.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="nsew")  # Expand all ways
        self.text_box.configure(background="#E9DCD6", borderwidth=2, relief="sunken")
        self.text_box.tag_configure("bold", font=("Helvetica",16,"bold"), foreground="black")  # Bold style for left column

        # Configure row and column weights
        for i in range(7):  # 7 rows
            root.rowconfigure(i, weight=1)
        for i in range(3):  # 3 columns
            root.columnconfigure(i, weight=1)

        # Configure row and column weights
        for i in range(7):  # 7 rows
            root.rowconfigure(i, weight=1)
        for i in range(2):  # 2 columns
            root.columnconfigure(i, weight=1)
        
        root.configure(bg=bg_color)
        

    def save_hotels_to_csv(self, hotels_list, filename):
        # Create the CSV file and write the header line
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['name', 'review_score','secondary_review_score','price', 'address', 'distance', 'city']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            # Write data for each hotel
            for hotel in hotels_list:
                writer.writerow(hotel)

    def date_validation(self, checkin_date, checkout_date):
        current_date = datetime.now()
        if checkin_date < current_date or checkout_date < current_date:
            messagebox.showerror("Error", "Check-in or Check-out date cannot be in the past.")
            return False
        
        # Checkin date should be after the checkout date
        if checkin_date >= checkout_date:
            messagebox.showerror("Error", "Check-in date must be before Check-out date.")
            return False
        
        return True


    def search_hotels(self):
        self.text_box.delete(1.0, tk.END)  # Clear any previous text
        
        city = self.city_var.get()
        # Date validation
        checkin_date = self.checkin_calendar.get_date()
        formatted_checkin_date = datetime.strptime(checkin_date, "%m/%d/%y")
        checkout_date = self.checkout_calendar.get_date()
        formatted_checkout_date = datetime.strptime(checkout_date, "%m/%d/%y")
        
        if not self.date_validation(formatted_checkin_date, formatted_checkout_date):
            return
        currency = self.currency_var.get()
        sort_by = self.sort_by_var.get()  # Get the selected sorting method
        
        # Different cities have different destination id's
        dest_id = {
            "Roma": 126693,
            "Stockholm": 2524279,
            "Venice": 132007,
            "Warsaw": 534433,
            "Helsinki": 1364995,
            "Amsterdam": 2140479,
            "Vilnius": 2620663,
            "Paris": 1456928,
            "Fulda": 1772866,
            "Liverpool": 2601422,
            "Berlin": 1746443,
            "Seoul": 716583,
            "Frankfurt": 1771148,
            "Kyoto": 235402
        }
        if (city not in dest_id.keys()):
            messagebox.showerror("Error","City Not Found!")
            return
        # Web scraping area
        url = f"https://www.booking.com/searchresults.en-gb.html?ss=Roma&ssne=Roma&ssne_untouched=Roma&efdco=1&label=gen173nr-1FCAQoggJCC3NlYXJjaF9yb21lSDNYBGjkAYgBAZgBKLgBF8gBDNgBAegBAfgBEIgCAagCA7gCzfPHsQbAAgHSAiRjYjQ3MDI5My03MWY3LTRhNDQtYTBmOC03NDVmODhhNmMyYmTYAgXgAgE&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-{dest_id[city]}&dest_type=city&checkin={formatted_checkin_date}&checkout={formatted_checkout_date}&group_adults=2&no_rooms=1&group_children=0&soz=1&lang_changed=1"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/51.0.2704.64 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        hotels_data = []
        sorted_hotels = []

        # Loop over the hotel elements and extract the desired data
        for hotel in hotels:
            # Extract the hotel name
            name_element = hotel.find('div', {'data-testid': 'title'})
            name = name_element.text.strip()

            # Extract the distance to center 
            distance_element = hotel.find("span",{"data-testid": "distance"})
            distance_to_center = distance_element.text.strip()

            # Extract the address
            address_element = hotel.find("span", {"data-testid" : "address"})
            address = address_element.text.strip()

            # Extract the review score
            review_score_element = hotel.find("div", {"data-testid":"review-score"})
            if review_score_element:
                review_score_text = review_score_element.text.strip()
                parts = review_score_text.split("Scored ")
                review_score = parts[1].split()[0]  
                review_info = parts[1].split(maxsplit=2)[1]  # just take review info
                review_type = review_info.split()[0]  # review type
            else:
                review_score = "N/A"
                review_type = ""
            if review_type == "Very":
                review_type = "Very Good"

           # Extract the price
            price_tag = hotel.find("span", {"data-testid": "price-and-discounted-price"})

            if price_tag:
                price = price_tag.text
                price = price.replace("TL", "").replace(",", "").replace("\xa0", "").replace(".", "").strip()
                price = int(price)
            else:
                price = "N/A" 

            
            # Extract the secondary review score(rating)
            secondary_review_score = hotel.find('span', class_='a3332d346a')
            if secondary_review_score:
                secondary_review_score_text = secondary_review_score.text.strip()
                print(secondary_review_score_text)
                
            else:
                secondary_review_score_text = "N/A"

            # Append hotels_data with info about hotel
            hotels_data.append({
                'name': name,
                'review_score': review_score + " " + review_type,
                'secondary_review_score': secondary_review_score_text,  # Include secondary review score
                'price': price,
                'address': address,
                'distance': distance_to_center,
                'city': city
            })

        # Sort hotels_data based on the selected sorting method
        if sort_by == "Review Score":
            sorted_hotels = sorted(hotels_data, key=lambda x: x['review_score'], reverse=True)
        elif sort_by == "Secondary Review Score":
            sorted_hotels = sorted([hotel for hotel in hotels_data if hotel['secondary_review_score'] != 'N/A'], 
                                   key=lambda x: float(x['secondary_review_score'].split(' ')[-1]), reverse=True)

        # Select top 5 hotels
        sorted_hotels = sorted_hotels[:self.top_var.get()]

        # Write the best hotels in the text box
        counter = 1
        for hotel in sorted_hotels:
            self.text_box.insert(tk.END, f"\n HOTEL {counter}\n", "bold")
            self.text_box.insert(tk.END, f" Name: ", "bold")
            self.text_box.insert(tk.END, f"{hotel['name']}\n")
            self.text_box.insert(tk.END, f" Address: ", "bold")
            self.text_box.insert(tk.END, f"{hotel['address']}\n")
            self.text_box.insert(tk.END, f" Distance: ", "bold")
            self.text_box.insert(tk.END, f"{hotel['distance']}\n")
            self.text_box.insert(tk.END, f" Review Score: ", "bold")
            self.text_box.insert(tk.END, f"{hotel['review_score']}\n")
            self.text_box.insert(tk.END, f" Secondary Review Score: ", "bold")
            self.text_box.insert(tk.END, f"{hotel['secondary_review_score']}\n")
            hotel_price = hotel["price"]
            if currency == "Euro":
                converted_price = round(hotel_price / 30)
                self.text_box.insert(tk.END, f" Price: ", "bold")
                self.text_box.insert(tk.END, f"{converted_price} Euro\n")
            else: 
                self.text_box.insert(tk.END, f" Price: ", "bold")
                self.text_box.insert(tk.END, f"{hotel_price} TL\n")
            """ self.text_box.insert(tk.END, f"City: ", "bold")
            self.text_box.insert(tk.END, f"{hotel['city']}\n")
            self.text_box.insert(tk.END, f"Check-in Date: ", "bold")
            self.text_box.insert(tk.END, f"{checkin_date}\n")
            self.text_box.insert(tk.END, f"Check-out Date: ", "bold")
            self.text_box.insert(tk.END, f"{checkout_date}\n")
            self.text_box.insert(tk.END, f"Base price: ", "bold")
            self.text_box.insert(tk.END, f"{hotel_price} TL\n") """
            counter += 1

        # Save top 5 hotels to CSV file
        self.save_hotels_to_csv(sorted_hotels, 'myhotels.csv')

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelScraperApp(root)
    root.mainloop()
