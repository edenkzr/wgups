                                        #Diego Cuadros | 011746822 | dcuadro@wgu.edu
import csv
import datetime

#class for hash table with collision handling capabilities via chaining and resizing [Overall Time: O(n) but Average and likely O(1) , Space O(n)]
class ChainingHashTable:

    #Hash table constructor
    def __init__(self, capacity = 40):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    #method for insertions and updates
    def insert(self, key, value):

        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True

        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    #search via key
    def search(self, key):

        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]

        return None

    #remove via key
    def remove(self, key):

        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv[0], kv[1])

#Class representing package information with attributes listed for routing and tracking purposes [Overall Time: O(1), Space: O(1)]
class Package:

    #Constructor [Time: O(1) package initialization, Space: O(1) package is a fixed amount of space]
    def __init__(self, package_ID, address, city, state, zip, delivery_deadline, weight, constraint):
        self.package_ID = package_ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.constraint = constraint
        self.status = "at hub"
        self.delivery_time = None
        self.departure_time = None

    #Override print to show detailed package data  [Time: O(1) string formatting with fixed data, Space: O(1) string is a fixed amount of space]
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_ID, self.address, self.city, self.state,
                                                               self.zip, self.delivery_deadline, self.weight,
                                                               self.constraint, self.status, self.delivery_time, self.departure_time)

#Class representing trucks utilized for package delivery services with attributes for tracking and routing purposes [Overall Time: O(1), Space: O(1)]
class Truck:

    #Constructor only takes 2 arguments that must be verified with respect to constraints. [Time: O(1) package initialization, Space: O(1) package is a fixed amount of space]
    def __init__(self, departure_time, packages):

        if departure_time < datetime.timedelta(hours=8): #verify trucks cant leave earlier than 8.
            raise ValueError("Trucks cannot depart before 8:00 A.M.")
        if len(packages) > 16: #verify trucks cant carry more than 16 packages
            raise ValueError("Trucks cannot carry more than 16 packages.")
        self.speed = 18.0
        self.miles = 0.0
        self.current_stop = "4001 South 700 East"
        self.time = departure_time
        self.departure_time = departure_time
        self.packages = packages
        self.route = []

    #Override print to show detailed truck data [Time: O(1) string formatting with fixed data, Space: O(1) string is a fixed amount of space]
    def __str__(self):
        return ("Mph: %s ,Total miles: %s, Last stop: %s, Time of completion: %s, Departed at: %s, Packages: %s, Route taken: "
                "%s" %
                (self.speed, self.miles, self.current_stop, self.time, self.departure_time, self.packages, self.route))

#Load Hash Table with package objects [Overall Time: O(n), Space: O(n)]
def loadPackageData(file_name):

    #Load from csv necessary attribute information [Time: O(n) n number of packages in a csv file, Space: O(n) creating n objects and storing in hash table]
    with open(file_name) as Packages:
        packageData = csv.reader(Packages, delimiter=',')
        next(packageData)
        for package in packageData:
            package_ID = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_delivery_deadline = package[5]
            package_weight = package[6]
            if package[7]: #if there is a constraint take it else its None
                package_constraint = package[7]
            else:
                package_constraint = None

            p = Package(package_ID, package_address, package_city, package_state, package_zip,
                        package_delivery_deadline, package_weight, package_constraint)

            #insert key value pair to hash table
            h.insert(package_ID, p)
            #print(p)

#Load distance information into 2D dictionary 'distance matrix' [Overall Time: O(n*m), Space: O(n*m)]
def loadDistance(file_name):

    #Load csv information into 2d dictionary [Time: O(n*m) n rows times m columns per csv file, Space: O(n*m) store n times m distance values]
    distances = {}
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)

        #Strip ensures consistency. Loop adds first row as keys like normal, continue adding dictionaries as the values,
        #add value if there is a value to be added, else None
        for row in reader:
            key = row[0].strip()
            distances[key] = {headers[i]: float(row[i]) if row[i] else None for i in range(1, len(row))}

    return distances

#Utilize distance matrix to quickly find distance values between point a and point b [Overall Time: O(1)], Space: O(1)]
def findDistance(a,b):

    #if distance comes up as None, invert the inputs [Time: O(1) dictionary look up is always constant , Space: O(1) assigngments and ifs are constant]
    distance = distance_matrix[a][b]
    if distance == None:
        distance = distance_matrix[b][a]
    return distance

#Main algorithm for routing 'Nearest Neighbor' [Overall Time: O(n^2), Space: O(n)]
def packageDelivery(truck):

    #Generate package objects from truck package list [Time: Worst case O(n^2), Average O(n) for n ids in truck list, Space: O(n) create routing list with n objects]
    routing = []
    route = []
    for ID in truck.packages:
        package = h.search(ID)
        routing.append(package)

    #While we still have packages, continually update next_stop and next_package information for necessary sorting and arithmetic operations
    #[Time: O(n^2) while n > 0 iterate through n packages to find the next stop, Space O(n): create route list with n packages according to findDistance comparisons]
    while len(routing) > 0:
        next_stop = float("inf")
        next_package = None

        #Find the nearest package to current location of the truck
        for package in routing:
            if findDistance(truck.current_stop, package.address) <= next_stop:
                next_stop = findDistance(truck.current_stop, package.address)
                next_package = package
        route.append(next_package.package_ID)
        routing.remove(next_package)
        truck.miles += next_stop #keep summing miles for final calculations
        truck.current_stop = next_package.address #keep track of where the truck is at
        truck.time += datetime.timedelta(hours=next_stop / truck.speed) #track the truck's time on the road
        next_package.delivery_time = truck.time #record package delivery_time for tracking purposes
        next_package.departure_time = truck.departure_time #record package departure_time for tracking purposes

    truck.route = route

    #check algorithm is working properly
    """for id in route:
        print(h.search(id))

    print(truck)"""
    
#Retrieve and change status information of specified packages at specified times [Overall Time: O(n), Space: O(1)]
def updateStatus(package_ID, time):

    #return package for time comparison [Time: o(n) hash table worst case is linear but average is O(1), Space: O(1) constant space used]
    package = h.search(package_ID)
    if time < package.departure_time:

        #packages are pre-set to be 'at hub'
        return package.status

    elif package.departure_time <= time < package.delivery_time:

        package.status = "en route"
        return package.status

    else:

        package.status = "delivered"
        return package.status

#Load all necessary data structures and class objects for program functionality
h = ChainingHashTable()
loadPackageData("wgups_packages.csv")
distance_matrix = loadDistance('wgups_distances.csv')
truck1 = Truck(datetime.timedelta(hours=9, minutes=5), [1,6,25,13,40,26,34,17,29])
truck2 = Truck(datetime.timedelta(hours=8), [14,15,16,20,19,3,18,36,37,5,38,31,30,7,35])
truck3 = Truck(datetime.timedelta(hours=10, minutes=20), [9,8,39,28,32,33,2,4,10,11,12,21,22,23,24,27])
t1 = packageDelivery(truck1)
t2 = packageDelivery(truck2)
t3 = packageDelivery(truck3)

#tests
"""for i in range(len(h.table)):
   print("Key: {} and Package: {}".format(i+1, h.search(i+1)))

for key, row in distance_matrix.items():
    print(f"[ {key} , {row} ]")

test_package = h.search(1)
test_package2 = h.search(40)
print(test_package.address)
print(test_package2.address)
print(findDistance(package.address, package2.address))
test_delivery = packageDelivery(truck1)
for i in range(1,41):
    time = datetime.timedelta(hours=10)
    status = updateStatus(i, time)
    print(f"At {time}, package {i} was {status}.")"""

#Continous Loop for UI purposes [Overall Time:O(1), Space: O(1)]
#UI loop itself doesnt introduce any significant time or space usages as its a simple I/O system
print("Welcome to WGUPS!")
while True:

    response = input("Please select an option from the following:\n1. Display truck information.\n2. Display package tracking information."
                     "\n3. Display package delivery time.\n4. exit.\nChoose here:"
                     )

    if response == "1":

        choice = input("Select an option:\n1. Display total mileage.\n2. Display details of trucks.\nChoose here: ")

        if choice == "1":

            miles = truck1.miles + truck2.miles + truck3.miles
            print(f"Total miles travelled: {miles}\n1"
                  f"")

        if choice == "2":

            print(f"Truck 1 details: {truck1}")
            print(f"Truck 2 details: {truck2}")
            print(f"Truck 3 details: {truck3}\n")

    elif response == "2":

        try:

            id = int(input("Enter a valid package ID: "))

            if 1 <= id <= len(h.table):

                time = input("Enter package delivery time 'format HH:MM': ")
                hour,min = time.split(":")
                requested_time = datetime.timedelta(hours=int(hour), minutes=int(min))
                status = updateStatus(id, requested_time)
                print(f"At {time}, package {id} was {status}.\n")

            else:

                print("Invalid package ID.[1-40]")

        except ValueError:

            print("Invalid input. Please enter a valid package ID.[1-40]2")


    elif response == "3":

        try:

            id = int(input("Enter a valid package ID: "))

            if 1 <= id <= len(h.table):

                result = h.search(id)
                print(f"Package {id} was delivered at {result.delivery_time}, deadline at {result.delivery_deadline}.\n")

            else:

                print("Invalid package ID.[1-40]")

        except ValueError:

            print("Invalid input. Please enter a valid package ID.[1-40]")

    elif response == "4":

        print("Goodbye!")
        break

    else:

        print("Please select from the provided options 'Type 1 - 4'.")


1
