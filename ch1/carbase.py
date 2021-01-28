
from os.path import splitext
import csv

def separate_whl(body):
    whl = body.split("x")
    return whl

    

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    
    def get_photo_file_ext(self):
        ext = splitext(self.photo_file_name)[1]   
        return ext


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'



class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        body = separate_whl(body_whl)
        try:
            self.body_length = float(body[0])
            self.body_width = float(body[1])
            self.body_height = float(body[2])
        except ValueError:
            self.body_length = 0
            self.body_width = 0
            self.body_height = 0
        
        self.car_type = 'truck'

    def get_body_volume(self):
        return self.body_height*self.body_length*self.body_width

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        try:
            for row in reader:
                if row[0] == 'car':
                    car_list.append(Car(row[1],row[3],row[5],row[2]))
                elif row[0] == 'truck':
                    car_list.append(Truck(row[1],row[3],row[5],row[4]))
                elif row[0] == 'spec_machine':
                    car_list.append(SpecMachine(row[1],row[3],row[5],row[6]))
        except IndexError:
            pass
        
    return car_list
