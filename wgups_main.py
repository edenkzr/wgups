import csv


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

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_ID, self.address, self.city, self.state, self.zip, self.delivery_deadline, self.weight, self.constraint, self.status)

class Truck:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.currentLocation, self.time, self.departTime, self.packages)

def loadPackageData(fileName):
    with open(fileName) as Packages:
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

def loadDistance(fileName):
    distances = {}
    with open(fileName, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)

        for row in reader:
            key = row[0].strip()
            distances[key] = {headers[i]: float(row[i]) if row[i] else None for i in range(1, len(row))}

    return distances

def findDistance(a,b):
    distance = distanceMatrix[a][b]
    if distance == None:
        distance = distanceMatrix[b][a]
    return distance



h = ChainingHashTable()
loadPackageData("wgups_packages.csv")
distanceMatrix = loadDistance('wgups_distances.csv')

"""for i in range(len(h.table)):
   print("Key: {} and Package: {}".format(i+1, h.search(i+1)))

for key, row in distanceMatrix.items():
    print(f"[ {key} , {row} ]")"""

package = h.search(1)
package2 = h.search(40)
print(package.address)
print(package2.address)


print(findDistance(package.address, package2.address))
