# Name: Matt Holmstrom
# OSU Email: holmstrm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Implementing a HashMap class using separate chaining
# Due Date: 2/14/2024
# Description: This program implements a HashMap class using separate chaining for collision resolution.
# The HashMap class uses a DynamicArray to store the hash table, and uses separate chaining using
# singly-linked lists for the collision resolution. Chains of keys and their corresponding values are stored as
# list nodes. This is an optimized HashMap, which means that the average case performance of all its
# operations is limited to an O(1) time complexity. Some of the methods that the class contains are
# put, remove, get_keys_and_values, and resize_table.




from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        of the table is greater than or equal to 1, then the resized method is called, which
        then doubles the hash maps current capacity.
        """

        load_factor = self.table_load()
        if load_factor >= 1.0 :  # if the load factor is greater than 1.0, then double the capacity of the hash table
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)
        index = hash % self._capacity # this is the index in the hash table that corresponds to the given key/value pair
        linked_list = self._buckets.get_at_index(index) # this is the linked list at the index in the hash table that corresponds to the key/value pair.
        list_size = linked_list.length()
        if list_size == 0: # if the linked list contains no key/value pairs, then just insert a new node containing the new key/value pair into the list.
            linked_list.insert(key, value)
            self._size +=1
            return

        if list_size != 0 and linked_list.contains(key)== None: # if the linked list is not empty, and does not contain the given key, then just insert a new node containing the new key/value pair into the list.
            linked_list.insert(key, value)
            self._size +=1
            return

        if list_size != 0 and linked_list.contains(key) != None: # if the linked list is not empty, and contains the given key, then replace that key's value with the given value.
                for list_node in linked_list:
                    if list_node.key == key:
                        list_node.value = value # in this case, we don't increase the hash map's size.

    def resize_table(self, new_capacity: int) -> None:
        """
        This method takes a new capacity as its parameter. The method changes the hash table's
        underlying capacity. All the existing key/value pairs are inserted into the new table, which
        means that all the hash table links are rehashed. If the given new capacity is less than 1,
        then the method does nothing. If the given new capacity is greater than 1, then the method
        makes sure it is a prime number. If the given capacity is prime, then the method changes the
        hash table's underlying capacity.
        """

        if new_capacity < 1: # if the given capacity is less than 1, then don't do anything
            return

        else:
            if new_capacity == 2: # if the given capacity is 2 (this is an edge case), then don't call the next_prime method
                self._capacity == 2
            else:
                new_capacity = self._next_prime(new_capacity) # if the new capacity is prime, then we use that capacity, if otherwise, then we find the next prime.
            buckets = self._buckets # variable to hold the hash maps previous buckets
            buckets_size = buckets.length()
            index1 = 0
            self._buckets = DynamicArray() # clear the content's of the hash table
            self._size = 0 # reset the hash table's size to 0
            self._capacity = new_capacity # set the hash table's capacity to the given capacity

            while index1 < new_capacity: # refill the hash map with empty linked lists (in the amount of the given capacity)
                self._buckets.append(LinkedList())
                index1 += 1

            index2 = 0
            while index2 < buckets_size: # this loop will take the hash maps previous contents, and insert it into the hash map after the capacity has been updated
                if buckets[index2].length() == 0: # if the link list is empty, there is no need to add it.
                    index2 +=1
                    continue
                else: # if the linked list is not empty, then insert the previous key/value pairs into the updated hash map.
                    linked_list = buckets.get_at_index(index2)
                    for list_node in linked_list:
                        self.put(list_node.key, list_node.value)
                index2 +=1

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
        count = 0 # used to keep count of the empty buckets
        index = 0
        hash_map_capacity = self.get_capacity()
        while index < hash_map_capacity: # iterate through the hash table and count all the empty linked lists.
            linked_list = self._buckets.get_at_index(index)
            if linked_list.length() == 0: # if the linked list is empty, then the bucket is empty.
                count += 1 # add 1 to the count
            index += 1
        return count

    def get(self, key: str):
        """
        This method takes a key as its parameter. The method returns the value
        associated with the given key. If the given key is not in the hash map,
        then the method returns None.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity # the index of the bucket which possibly contains given key
        linked_list = self._buckets.get_at_index(index) # get the specific bucket that possibly contains the given key
        for list_node in linked_list: # iterate through the linked list, and if a node in the linked list contains the given key, then return its associated value
            if list_node.key == key:
                return list_node.value

        return None # The key isn't in the hash map, so just return None

    def contains_key(self, key: str) -> bool:
        """
        This method takes a key as its parameter. The method returns True if
        the key is in the hash map, and False if otherwise. If the hash map is empty,
        then the method returns False.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity # the index of the bucket which possibly contains given key
        linked_list = self._buckets.get_at_index(index) # get the specific bucket that possibly contains the given key
        for list_node in linked_list: # iterate through the linked list, and if a node in the linked list contains the given key, then return True
            if list_node.key == key:
                return True

        return False # The key isn't in the hash map, so just return False

    def remove(self, key: str) -> None:
        """
        This method takes a key as its parameter. If the given key exists in the hash map
        then the method removes the key's associated value. If the given key does not exist
        in the hash map, then the method does nothing.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        linked_list = self._buckets.get_at_index(index) # get the specific bucket that possibly contains the given key
        if linked_list.contains(key) is not None: # if the linked lists's contain method returns the key, then remove the node containing that key.
            for list_node in linked_list:
                if list_node.key == key: # if the given key matches the key in node, then remove it and its value
                    linked_list.remove(key)
                    self._size -=1 # decrease the map's size by 1
        else: # else, the key was not found, so the method does nothing.
            return


    def get_keys_and_values(self) -> DynamicArray:
        """
        This method takes no parameters. The method returns a DynamicArray of tuples,
        where each tuple contains a key and its associated value, which are currently
        stored in the hash map.
        """

        key_value_arr = DynamicArray() # create a DynamicArray which will contain the tuples of key/value pairs
        index = 0
        while index < self._buckets.length() : # iterate through the buckets
                linked_list = self._buckets[index]
                for list_node in linked_list: # iterate through all the nodes in the linked list, and append their associated key/value pairs into the array
                    key_val_tuple = (list_node.key, list_node.value)
                    key_value_arr.append(key_val_tuple) # append the tuple containing the key/value pair
                index +=1

        return key_value_arr # return the array

    def clear(self) -> None:
        """
        This method takes no parameters. The method clears the content that is
        currently in the hash map. The method does not change the hash table's
        underlying capacity.
        """
        linked_list = LinkedList()
        index = 0
        while index < self._capacity: # iterate through the hash table's capacity and make each bucket an empty linked list
            self._buckets[index] = linked_list
            index +=1
        self._size = 0 # reset the size to 0

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function takes a DynamicArray as its parameter (which is not necessarily sorted).
    The function returns a tuple which contains (in this order) a DynamicArray
    containing the mode or modes of the array passed into the function, and an integer representing
    the frequency that the mode or modes appeared in the given DynamicArray. The method is implemented
    with O(N) runtime complexity.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap

    new_map = HashMap() # hash map used to help find the mode or modes in the given array.
    index1 = 0
    dyn_arr_length = da.length()
    while index1 < dyn_arr_length: # iterate through the given array and insert each value and the number of times that value occurs, into the hash map
        count = 1 # by default the count of each value will be 1
        if new_map.contains_key(da[index1]) == True: # if the hash map already contains the value from the array, then increase its associated count by 1
            count = new_map.get(da[index1]) + 1
            new_map.put(da[index1], count) # add the value and its count into the hash map
        else: # if the value from the given array, isn't already in the hash map, then place the value in the hash map and the count of 1
            new_map.put(da[index1], count)
        index1 +=1

    frequency = 0 # use to keep track of the mode or modes frequency
    modes = DynamicArray() # an array which will store the mode or modes.
    keys_values = new_map.get_keys_and_values() # creates an array containing key/value pairs in tuples, where the key/value pairs are from the hash map
    index2 = 0
    for index2 in range(keys_values.length()): # iterate the key_value array:
        value = keys_values[index2][1] # get the value in the tuple
        key = keys_values[index2][0] # get the key in the tuple
        if value > frequency: # if the value is larger than the current frequency then update the modes array
            modes = DynamicArray() # clear the modes array
            modes.append(key) # append this key, this is a possible mode
            frequency = value # update the frequency
        elif value < frequency: # if the value is less than the highest frequency then move on.
            continue
            index2 +=1
        else:
            modes.append(key) # if the value equals the frequency, then append the key to the modes array (this means that there could be more than one mode possibly)
        index2 += 1

    modes_frequency_tuple = (modes, frequency)
    return modes_frequency_tuple



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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
