from app.SmartServices.Restaurant.RestaurantService import RestaurantService

def start_restaurant_service():
    restaurant = RestaurantService("Hotel Restaurant", "localhost", 1883)
    return restaurant