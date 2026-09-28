"""
Title: Movie Ticket Inventory Management System
Author: Student Developer
Description: A modular Python application built to satisfy VITyarthi project rules.
             Implements three core functional modules and explicit error handling.
"""

import sys

class MovieInventoryModule:
    """Manages the movies, showtimes, and individual seat allocation counts."""
    def __init__(self):
        # Seed data to provide immediate out-of-the-box system interaction
        self.inventory = {
            101: {"title": "Inception", "time": "14:00", "price": 12.50, "seats": 50, "sold": 0},
            102: {"title": "Interstellar", "time": "18:30", "price": 15.00, "seats": 35, "sold": 0},
            103: {"title": "The Dark Knight", "time": "21:00", "price": 14.00, "seats": 8, "sold": 0}
        }

    def display_available_movies(self):
        print("\n--- Current Live Movie Schedule & Inventory ---")
        print(f"{'ID':<6}{'Movie Title':<20}{'Showtime':<10}{'Price':<10}{'Available Seats':<15}")
        print("-" * 65)
        for movie_id, data in self.inventory.items():
            print(f"{movie_id:<6}{data['title']:<20}{data['time']:<10}${data['price']:<9.2f}{data['seats']:<15}")
        print("-" * 65)

    def add_new_movie(self, movie_id, title, showtime, price, capacity):
        if movie_id in self.inventory:
            return False, "Movie ID already exists in system records."
        
        self.inventory[movie_id] = {
            "title": title,
            "time": showtime,
            "price": float(price),
            "seats": int(capacity),
            "sold": 0
        }
        return True, f"Successfully listed '{title}' into inventory."


class BookingEngineModule:
    """Processes ticket selection, checks availability constraints, and processes sales."""
    def __init__(self, inventory_module):
        self.inv_mod = inventory_module
        self.total_transactions_processed = 0

    def process_booking(self, movie_id, ticket_count):
        # Security & Input Validation Checks
        if movie_id not in self.inv_mod.inventory:
            return False, "Error: The requested Movie ID cannot be located."
        
        if ticket_count <= 0:
            return False, "Error: Booking quantity must be at least 1 ticket."

        movie = self.inv_mod.inventory[movie_id]
        
        if movie["seats"] == 0:
            return False, f"Booking Failed: '{movie['title']}' is completely sold out!"
        
        if ticket_count > movie["seats"]:
            return False, f"Booking Failed: Insufficient seats remaining. Only {movie['seats']} seats left."

        # Executing inventory adjustment
        movie["seats"] -= ticket_count
        movie["sold"] += ticket_count
        
        total_cost = ticket_count * movie["price"]
        self.total_transactions_processed += 1
        
        invoice_details = (
            f"\n=== TRANSACTION RECEIPT ===\n"
            f"Movie: {movie['title']}\n"
            f"Showtime: {movie['time']}\n"
            f"Tickets Issued: {ticket_count}\n"
            f"Total Charged: ${total_cost:.2f}\n"
            f"==========================="
        )
        return True, invoice_details


class ReportingAnalyticsModule:
    """Compiles revenue summaries and monitors capacity utilization tracking."""
    def __init__(self, inventory_module):
        self.inv_mod = inventory_module

    def render_management_dashboard(self):
        print("\n================ ADMINISTRATIVE METRICS DASHBOARD ================")
        total_revenue = 0.0
        total_tickets_sold = 0
        
        print(f"{'Movie Title':<20}{'Tickets Sold':<15}{'Revenue Generated':<20}{'Occupancy state':<15}")
        print("-" * 72)
        
        for m_id, data in self.inv_mod.inventory.items():
            movie_revenue = data["sold"] * data["price"]
            total_revenue += movie_revenue
            total_tickets_sold += data["sold"]
            
            total_capacity = data["seats"] + data["sold"]
            occupancy_pct = (data["sold"] / total_capacity * 100) if total_capacity > 0 else 0
            
            status_flag = "STABLE"
            if data["seats"] == 0:
                status_flag = "SOLD OUT"
            elif occupancy_pct >= 75:
                status_flag = "HIGH DEMAND"

            print(f"{data['title']:<20}{data['sold']:<15}${movie_revenue:<19.2f}[{status_flag}]")
            
        print("-" * 72)
        print(f"Cumulative Corporate Revenue : ${total_revenue:.2f}")
        print(f"Total Physical Tickets Sold  : {total_tickets_sold}")
        print("=================================================================\n")


def main():
    """Main program entry point orchestrating workflow interaction loops."""
    # Instantiate modules demonstrating proper architectural modularity
    inventory_system = MovieInventoryModule()
    booking_engine = BookingEngineModule(inventory_system)
    analytics_system = ReportingAnalyticsModule(inventory_system)

    print("Welcome to the Movie Ticket Inventory Management System")
    
    while True:
        print("\n--- Main Operational Menu ---")
        print("1. View Scheduled Movies & Inventory Availability")
        print("2. Purchase Customer Movie Tickets")
        print("3. View Admin Financial & Analytics Dashboard")
        print("4. Register a New Movie Listing into System")
        print("5. Terminate Application System")
        
        user_choice = input("Select an option range (1-5): ").strip()
        
        if user_choice == "1":
            inventory_system.display_available_movies()
            
        elif user_choice == "2":
            inventory_system.display_available_movies()
            try:
                m_id = int(input("Enter target Movie ID to buy tickets: "))
                count = int(input("Enter number of tickets to purchase: "))
                
                success, response_msg = booking_engine.process_booking(m_id, count)
                print(response_msg)
            except ValueError:
                print("Input Error: Please pass valid numerical values for IDs and quantities.")
                
        elif user_choice == "3":
            analytics_system.render_management_dashboard()
            
        elif user_choice == "4":
            print("\n--- Admin: Register New Movie Space ---")
            try:
                new_id = int(input("Assign unique integer ID: "))
                title = input("Enter movie title name: ").strip()
                time_slot = input("Set showtime format (e.g. 19:15): ").strip()
                price = float(input("Set base ticket price cost: $"))
                capacity = int(input("Set max room seating capacity: "))
                
                if not title or not time_slot:
                    print("Error: Name string entries cannot remain blank.")
                    continue
                    
                success, outcome = inventory_system.add_new_movie(new_id, title, time_slot, price, capacity)
                print(outcome)
            except ValueError:
                print("Input Error: Numeric inputs must be configured accurately.")
                
        elif user_choice == "5":
            print("Shutting down Inventory Engines. Safe travels.")
            sys.exit(0)
            
        else:
            print("Invalid Menu selection. Please submit a figure from 1 to 5.")

if __name__ == "__main__":
    main()
