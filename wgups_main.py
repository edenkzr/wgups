import csv
import datetime

#class for hash table with collision handling capabilities via chaining
class ChainingHashTable:

    #constructor initializing table with empty lists
    def __init__(self, capacity = 40):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    #method for insertions and updates
    def insert(self, key, value):

        #assings an index generated via the built in hash function
        bucket = hash(key) % len(self.table)
        #assings whatever is in that index
        bucket_list = self.table[bucket]

        #check if kv pair already in bucket_list
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True

        #else append to bucket_list
        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    #method for searching via key
    def search(self, key):

        #figures out where this key would be in the list
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #search list via key and return value if found
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]

        #else return None
        return None

    #method for removing via key
    def remove(self, key):

        #figures out where this key would be in the list
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #search list via key and remove both kv if found
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv[0], kv[1])

class Package:
    def __init__(self, package_ID, address, city, state, zip, delivery_deadline, weight, constraint, status):
        self.package_ID = package_ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.constraint = constraint
        self.status = status
        self.delivery_time = None
        self.departure_time = None


    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_ID, self.address, self.city, self.state,
                                                               self.zip, self.delivery_deadline, self.weight,
                                                               self.constraint, self.status, self.delivery_time, self.departure_time)

class Truck:
    def __init__(self, departure_time, packages):
        self.speed = 18.0
        self.miles = 0.0
        self.current_stop = "4001 South 700 East"
        self.time = departure_time
        self.departure_time = departure_time
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.current_stop, self.time, self.departure_time, self.packages)

def loadPackageData(file_name):
    with open(file_name) as Packages:
        packageData = csv.reader(Packages, delimiter=',')
        next(packageData)
        for package in packageData:
            packageID = int(package[0])
            packageAddress = package[1]
            packageCity = package[2]
            packageState = package[3]
            packageZip = package[4]
            packageDeliveryDeadline = package[5]
            packageWeight = package[6]
            if package[7]:
                packageConstraint = package[7]
            else:
                packageConstraint = None
            packageStatus = "at hub"

            p = Package(packageID, packageAddress, packageCity, packageState, packageZip,
                        packageDeliveryDeadline, packageWeight, packageConstraint, packageStatus)

            h.insert(packageID, p)
            #print(p)

def loadDistance(file_name):
    distances = {}
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)

        for row in reader:
            key = row[0].strip()
            distances[key] = {headers[i]: float(row[i]) if row[i] else None for i in range(1, len(row))}

    return distances

def findDistance(a,b):
    distance = distance_matrix[a][b]
    if distance == None:
        distance = distance_matrix[b][a]
    return distance


def packageDelivery(truck):
    routing = []
    route = []

    for ID in truck.packages:
        package = h.search(ID)
        routing.append(package)

    while len(routing) > 0:
        next_stop = float("inf")
        next_package = None
        for package in routing:
            if findDistance(truck.current_stop, package.address) <= next_stop:
                next_stop = findDistance(truck.current_stop, package.address)
                next_package = package
        route.append(next_package.package_ID)
        routing.remove(next_package)
        truck.miles += next_stop
        truck.current_stop = next_package.address
        truck.time += datetime.timedelta(hours=next_stop / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time

    for id in route:
        print(h.search(id))

    print(truck)


h = ChainingHashTable()
loadPackageData("wgups_packages.csv")
distance_matrix = loadDistance('wgups_distances.csv')


truck1 = Truck(datetime.timedelta(hours=9, minutes=5), [1,6,25,13,40,26,34,17,29])
truck2 = Truck(datetime.timedelta(hours=8), [14,15,16,20,19,3,18,36,37,5,38,31,30,7,35])
truck3 = Truck(datetime.timedelta(hours=10, minutes=20), [9,8,39,28,32,33,2,4,10,11,12,21,22,23,24,27])
"""for i in range(len(h.table)):
   print("Key: {} and Package: {}".format(i+1, h.search(i+1)))

for key, row in distance_matrix.items():
    print(f"[ {key} , {row} ]")

package = h.search(1)
package2 = h.search(40)
print(package.address)
print(package2.address)


print(findDistance(package.address, package2.address))
"""

test1 = packageDelivery(truck1)
