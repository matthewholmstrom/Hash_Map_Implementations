# Name: Matt Holmstrom
# OSU Email: holmstrm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Implementing a HashMap class using open addressing
# Due Date: 2/14/2024
# Description: This program implements a HashMap class using open addressing with quadratic
# probing for collision resolution. The open addressing with quadratic probing for collision resolution,
# is done inside the DynamicArray. All the hash map's key/value pairs are stored in the dynamic array.
# This is an optimized HashMap, which means that the average case performance of all its
# operations is limited to an O(1) time complexity. Some of the methods that the class contains are
# put, remove, get_keys_and_values, and resize_table.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method takes a key and its associated value as parameters. The method updates
        the key/value pair in the hash map. If the given key is not in the hash map, then
        the given key/value pair is added to the hash map. If the given key already exists
        in the hash map, then its value is replaced with the given value. If the load factor
        of the table is greater than or equal to 0.5, then the resized method is called, which
        then doubles the hash maps current capacity.
        """

        if self.table_load() >= 0.5: # if the load factor is greater than 0.5, then double the capacity of the hash table.
            self.resize_table(self._capacity * 2)

        i_initial = self._hash_function(key) % self._capacity # get the initial index of the given key/value pair

        hash_entry = HashEntry(key, value) # create a new hash entry containing the given key and value
        entry = self._buckets.get_at_index(i_initial) # get the hash entry corresponding to the initial index
        j = 0
        quad_probe = i_initial

        while entry != None : # if the bucket corresponding to the given key/value pair is not empty then we possbily have a collision

            if entry.key == key or entry.is_tombstone is True: # if the buckets key is equal to the given key or the bucket's is_tombstone value is true, then exit the loop
                break
            j +=1 # else, if the initial bucket for the given key value pair is occupied by some other key/value pair and doesn't contain a tombstone, then use quadratic probing to find the next open bucket
            quad_probe = (i_initial + (j **2)) % self.get_capacity() # variable to hold the updated index
            entry = self._buckets.get_at_index(quad_probe) # get the bucket corresponding to updated index

        if self._buckets.get_at_index(quad_probe) == None: # if the bucket at the index is empty, then add the given key/value pair into that bucket
            self._buckets.set_at_index(quad_probe, hash_entry)
            self._size += 1

        else: # the hash entry at the index is not None
            if self._buckets.get_at_index(quad_probe).is_tombstone == True: # if the bucket at the index contains a tombstone, the add the given key/value pair into that bucket
                self._buckets.set_at_index(quad_probe, hash_entry)
                self._size += 1 # increase the hash maps size by 1

            if self._buckets[quad_probe].key == key and self._buckets[quad_probe].is_tombstone == False: # if the bucket already contains the key, the replace the key's value with the given value
                self._buckets.set_at_index(quad_probe, hash_entry) # we don't need to update the size of the map

    def resize_table(self, new_capacity: int) -> None:
        """
        This method takes a new capacity as its parameter. The method changes the hash table's
        underlying capacity. All the active key/value pairs are inserted into the new table, which
        means that all the non-tombstone hash table links are rehashed. If the given new capacity is less than
        the current number of elements in the hash map, then the method does nothing. If the given new
        capacity is valid, then the method makes sure it is a prime number. If the given capacity is prime,
        then the method changes the hash table's underlying capacity.
        """

        if self._size > new_capacity:  # if the given capacity is less than the current size, then don't do anything
            return

        new_capacity = self._next_prime(new_capacity) # this ensures new_capacity is a prime number
        new_table = HashMap(new_capacity, self._hash_function) # create a new hash map containing the new capacity
        dyn_arr = DynamicArray() # this will hold the bucket of the new hash map
        index1 = 0

        while index1 < new_capacity:
            dyn_arr.append(None) # make each eventual bucket initially None
            index1 +=1
        new_table._buckets = dyn_arr # update the buckets of the new hash map

        for bucket in self: # iterate over all the buckets of the current hash map, and insert all the key/value pairs into the new hash map
                new_table.put(bucket.key, bucket.value)

        # set current hash maps capacity, size, and buckets to the corresponding ones from the new hash map
        self._capacity, self._size, self._buckets = new_table._capacity, new_table._size, new_table._buckets


    def table_load(self) -> float:
        """
        This method takes no parameters. The method returns the hash table's current
        load factor. The load factor is the hash table's current size divided by its
        current capacity.
        """
        load_factor = self._size / self._capacity # the load factor is the hash map's size divided by its capacity.
        return load_factor

    def empty_buckets(self) -> int:
        """
        This method takes no parameters. The method returns the number
        of empty buckets that are currently in the hash table.
        """
        count = 0  # used to keep count of the empty buckets
        index = 0
        hash_map_capacity = self.get_capacity()
        while index < hash_map_capacity:  # iterate through the hash table and count all the empty buckets.
            bucket = self._buckets.get_at_index(index)
            if bucket == None:  # if the hash entry is None, then the bucket is empty.
                count += 1  # add 1 to the count
            index += 1
        return count
    def get(self, key: str) -> object:
        """
        This method takes a key as its parameter. The method returns the value
        associated with the given key. If the given key is not in the hash map,
        then the method returns None.
        """

        index = 0
        while index < self._capacity: # iterate through the maps capacity, and if a hash entry contains the given key, then return its associated value
            if self._buckets[index] is not None: # if the bucket is not empty, then check if the hash entries key matches the given key
                if self._buckets[index].key == key:  # if this is true, then check theif the entry has a tombstone
                      if self._buckets[index].is_tombstone == True:
                            index += 1
                            continue
                      if self._buckets[index].is_tombstone == False: # if this is true, then return the given keys value
                            return self._buckets[index].value
            index +=1

        return None # the key isn't in the hash map, so just return None

    def contains_key(self, key: str) -> bool:
        """
        This method takes a key as its parameter. The method returns True if
        the key is in the hash map, and False if otherwise. If the hash map is empty,
        then the method returns False.
        """
        found = False
        index = 0
        while index < self._capacity: # iterate through the maps capacity, and if a hash entry contains the given key, then return True
            if self._buckets[index] is not None: # if the bucket is not empty, then check if the hash entries key matches the given key
                if self._buckets[index].key == key:
                    if self._buckets[index].is_tombstone == True:
                            index +=1
                            continue
                    if self._buckets[index].is_tombstone == False: # if this is true, then we will return true
                            found = True # set found equal to true, then we will return true
            index += 1

        return found # return True or False depending on whether we found the given key in the hash map

    def remove(self, key: str) -> None:
        """
        This method takes a key as its parameter. If the given key exists in the hash map
        then the method removes the key's associated value. If the given key does not exist
        in the hash map, then the method does nothing.
        """

        index = 0
        while index < self._capacity: # iterate through the maps capacity, and if a hash entry contains the given key, then remove the key
            if self._buckets[index] is not None:
                if self._buckets[index].is_tombstone == True and self._buckets[index].key == key: # if the current bucket contains a tombstone, then continue the iterating
                    index +=1
                    continue
                if self._buckets[index].is_tombstone == False and self._buckets[index].key == key: # if the current bucket contains the given key, then remove the key
                    self._buckets[index].is_tombstone = True # we remove the given key/value pair by setting the tombstone date member to true, and decreasing the size of the hash map.
                    self._size -=1
            index +=1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method takes no parameters. The method returns a DynamicArray of tuples,
        where each tuple contains a key and its associated value, which are currently
        stored in the hash map.
        """

        key_vals_arr = DynamicArray() # create a DynamicArray which will contain the tuples of key/value pairs
        index = 0
        while index < self._capacity: # iterate through the maps capacity, and if a hash entry contains the given key, then add the key/value pair to the array
            if self._buckets[index] is not None:
                if self._buckets[index].is_tombstone == True:
                    index += 1
                    continue
                if  self._buckets[index].is_tombstone == False:  # if this true the current bucket contains an active key/value pair
                     key1 = self._buckets[index].key
                     value1 = self._buckets[index].value
                     key_vals_tuple = (key1, value1)
                     key_vals_arr.append(key_vals_tuple) # append the tuple containing the key/value pair
            index +=1

        return key_vals_arr # return the array

    def clear(self) -> None:
        """
        This method takes no parameters. The method clears the content that is
        currently in the hash map. The method does not change the hash table's
        underlying capacity.
        """
        self._size = 0  # reset the hash maps size to 0
        new_dyn_arr = DynamicArray()
        index = 0
        while index < self._capacity: # iterate through the hash table's capacity and make each bucket empty
            new_dyn_arr.append(None)
            index+=1

        self._buckets = new_dyn_arr # update the hash maps buckets to the DynamicArray containing empty hash entries

    def __iter__(self):
        """
        This method takes no parameters. The method enables the HashMap class to iterate
        over itself. The method initializes a variable (self._index) to track the
        iterator's progress through the contents of the hash map.
        """
        self._index = 0 # variable (self._index) to track the iterator's progress through the contents of the hash map.
        return self

    def __next__(self):
        """
        This method takes no parameters. The method returns the next item in the hash map
        based on the iterator's current location. The method only iterates over the active
        items, i.e. all the buckets with key/value pairs, where is_tombstone is set to False.
        """

        try:
            found = True # set found initially to true, to start the while loop
            while found:
                num = self._buckets[self._index] # get the current hash_entry
                self._index += 1 # update the iterators data member
                if num == None or num.is_tombstone == True: # if the current hash entry doesn't contain an active key/value pair, then continue the loop
                    continue
                if num is not None and num.is_tombstone == False: # if the current hash entry contains an active key/value pair, the return that key/value pair
                    found = False
        except DynamicArrayException: # if we get an index out of bounds error, then raise the StopIteration error
            raise StopIteration

        return num # return the hash entry



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
