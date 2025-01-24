import csv


#class for hash table with collision handling capabilities via chaining
class ChainingHashTable:

    #constructor initializing table with empty lists
    def __init__(self, capacity = 10):
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
    def __init__(self, package_ID, address, city, state, zip, delivery_deadline, weight):
        self.package_ID = package_ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.package_ID, self.address, self.city, self.state, self.zip, self.delivery_deadline, self.weight)

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

            p = Package(packageID, packageAddress, packageCity, packageState, packageZip,
                        packageDeliveryDeadline, packageWeight)

            print(p)

            h.insert(packageID, p)


h = ChainingHashTable()
loadPackageData("wgups_packages.csv")

for i in range(len(h.table)):
    print("Key: {} and Package: {}".format(i+1, h.search(i+1)))
