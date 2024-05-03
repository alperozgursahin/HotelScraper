from datetime import datetime
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import csv
from tkcalendar import Calendar

class HotelScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Scraper App")

        # City Selection
        self.city_label = ttk.Label(root, text="Select City:")
        self.city_label.grid(row=0, column=0, padx=10, pady=10)

        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(root, textvariable=self.city_var)
        self.city_combobox['values'] = ['Roma', "Stockholm","Venice","Warsaw","Helsinki","Amsterdam","Vilnius","Paris","Fulda","Liverpool","Berlin", "Seoul", "Frankfurt", "Kyoto"]  # These area for cities
        self.city_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Check-in Date
        self.checkin_label = ttk.Label(root, text="Check-in Date:")
        self.checkin_label.grid(row=1, column=0, padx=10, pady=10)

        self.checkin_calendar = Calendar(root, selectmode="day", year=2024, month=5, day=1)
        self.checkin_calendar.grid(row=1, column=1, padx=10, pady=10)

        # Check-out Date
        self.checkout_label = ttk.Label(root, text="Check-out Date:")
        self.checkout_label.grid(row=2, column=0, padx=10, pady=10)

        self.checkout_calendar = Calendar(root, selectmode="day", year=2024, month=5, day=1)
        self.checkout_calendar.grid(row=2, column=1, padx=10, pady=10)

        # Currency Toggle
        self.currency_label = ttk.Label(root, text="Currency:")
        self.currency_label.grid(row=3, column=0, padx=10, pady=10)

        self.currency_var = tk.StringVar(value="Euro")
        self.currency_toggle = ttk.Checkbutton(root, text="Euro", variable=self.currency_var, onvalue="Euro", offvalue="TL")
        self.currency_toggle.grid(row=3, column=1, padx=10, pady=10)

        # Search Button
        self.search_button = ttk.Button(root, text="Search", command=self.search_hotels)
        self.search_button.grid(row=4, columnspan=2, padx=10, pady=10)

        # Large Font for Hotel Names
        self.large_font = ("Helvetica", 10, "bold")

        # Text Box
        self.text_box = tk.Text(root, height=20, width=80,font=self.large_font)
        self.text_box.grid(row=5, columnspan=2, padx=10, pady=10)

        

    def save_hotels_to_csv(self, hotels_list, filename):
        # Create the CSV file and write the header line
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['name', 'rating', 'price', 'address', 'distance', 'city']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            # Write data for each hotel
            for hotel in hotels_list:
                writer.writerow(hotel)

    def search_hotels(self):
        self.text_box.delete(1.0, tk.END)  # Clear any previous text
        
        city = self.city_var.get()
        checkin_date = self.checkin_calendar.get_date()
        formatted_checkin_date = datetime.strptime(checkin_date, "%m/%d/%y").strftime("%Y-%m-%d")
        checkout_date = self.checkout_calendar.get_date()
        formatted_checkout_date = datetime.strptime(checkout_date, "%m/%d/%y").strftime("%Y-%m-%d")
        currency = self.currency_var.get()
        
        # Different cities have different destination id's
        dest_id = ""
        if city == "Roma":
            dest_id = 126693
        if city == "Stockholm":
            dest_id = 2524279
        if city == "Venice":
            dest_id = 132007
        if city == "Warsaw":
            dest_id = 534433
        if city == "Helsinki":
            dest_id = 1364995
        if city == "Amsterdam":
            dest_id = 2140479
        if city == "Vilnius":
            dest_id = 2620663
        if city == "Paris":
            dest_id = 1456928
        if city == "Fulda":
            dest_id = 1772866
        if city == "Liverpool":
            dest_id = 2601422
        if city == "Berlin":
            dest_id = 1746443
        if city == "Seoul":
            dest_id = 716583
        if city == "Frankfurt":
            dest_id = 1771148
        if city == "Kyoto":
            dest_id = 235402

        # Web scraping area
        url = f"https://www.booking.com/searchresults.en-gb.html?ss=Roma&ssne=Roma&ssne_untouched=Roma&efdco=1&label=gen173nr-1FCAQoggJCC3NlYXJjaF9yb21lSDNYBGjkAYgBAZgBKLgBF8gBDNgBAegBAfgBEIgCAagCA7gCzfPHsQbAAgHSAiRjYjQ3MDI5My03MWY3LTRhNDQtYTBmOC03NDVmODhhNmMyYmTYAgXgAgE&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-{dest_id}&dest_type=city&checkin={formatted_checkin_date}&checkout={formatted_checkout_date}&group_adults=2&no_rooms=1&group_children=0&soz=1&lang_changed=1"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/51.0.2704.64 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        hotels_data = []

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
            review_score_element = hotel.find("div", {"data-testid":"review-score"}).text.strip()
            parts = review_score_element.split("Scored ")
            rating = parts[1].split()[0]  
            review_info = parts[1].split(maxsplit=2)[1]  # sadece review bilgisini al
            review_type = review_info.split()[0]  # review type
            if review_type == "Very":
                review_type = "Very Good"

            # Extract the price
            price_tag = hotel.find("span", {"data-testid": "price-and-discounted-price"})

            if price_tag:
                price = price_tag.text
                # TL ve virgülü kaldırıp boşluklara göre ayır
                price = int(price.replace("TL", "").replace(",", "").replace("\xa0", "").replace(".", "").strip())
            else:
                price = "N/A"  # Fiyat bulunamazsa "N/A" (Not Available) olarak ayarlayın.
            
            # Append hotels_data with info about hotel
            hotels_data.append({
                'name': name,
                'rating': rating + " " + review_type,
                'price': price,
                'address': address,
                'distance': distance_to_center,
                'city': city  # Şehir adını elle belirtiyoruz, çünkü URL'den alamıyoruz
            })

        # Get ranked hotel list, select top 5 hotels
        sorted_hotels = sorted(hotels_data, key=lambda x: x['rating'], reverse=True)[:5]

        # Write the best 5 hotels in the text box
        counter = 1
        self.text_box.insert(tk.END, "Top 5 Hotels by Ratings\n")
        for hotel in sorted_hotels:
            self.text_box.insert(tk.END, f"\n************* HOTEL {counter} *************\n")
            self.text_box.insert(tk.END, f"Name: {hotel['name']}\n")
            self.text_box.insert(tk.END, f"Address: {hotel['address']}\n")
            self.text_box.insert(tk.END, f"Distance: {hotel['distance']}\n")
            self.text_box.insert(tk.END, f"Rating: {hotel['rating']}\n")
            hotel_price = hotel["price"]
            self.text_box.insert(tk.END, f"Base price: {hotel_price} TL\n")
            if currency == "Euro":
                converted_price = round(hotel_price / 30)
                self.text_box.insert(tk.END, f"Price: {converted_price} Euro\n")
            else: 
                self.text_box.insert(tk.END, f"Price: {hotel_price} TL\n")
            self.text_box.insert(tk.END, f"City: {hotel['city']}\n")
            self.text_box.insert(tk.END, f"Check-in Date: {checkin_date}\n")
            self.text_box.insert(tk.END, f"Check-out Date: {checkout_date}\n")
            counter += 1

        # Save top 5 hotels to CSV file
        self.save_hotels_to_csv(sorted_hotels, 'myhotels.csv')

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelScraperApp(root)
    root.mainloop()