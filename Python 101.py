# ----------------------------
# Working with Strings
# ----------------------------

def test_strings():
    print("Hello World")
    print("   /|")
    print("  / |")
    print(" /  |")
    print("/___|")
    
    Character_name = "Sam"
    Character_age = "55"
    
    print("There once was a man named " + Character_name + ",")
    print("He was " + Character_age + " years old.")
    print("He really liked the name " + Character_name + ",")
    print("But didn't like being " + Character_age + ".")
    print("giraffe\nacademy")
    print("Giraffe\"Academy")
    
    phrase = "Giraffe Academy"
    print(phrase + " is cool")
    print(phrase.lower())
    print(phrase.upper())
    print(phrase.isupper())
    print(phrase.upper().isupper())
    print(len(phrase))
    print(phrase[0])
    print(phrase)
    print(phrase.index("G"))
    print(phrase.index("Acade"))
    print(phrase.replace("Giraffe", "Elephant"))


# ----------------------------
# Working with Numbers
# ----------------------------


def test_numbers():
    print(2)
    print(-2.097)
    print(3 + 4.5)
    print(3 + 4 * 5)
    print(3 * (4 + 5))
    print(10 % 3)
    print(10 / 3)

    my_num = 5
    print(my_num)
    print(str(my_num))
    print(str(my_num) + " my favourite number")

    my_num = -5
    print(abs(my_num))
    print(pow(3, 2))
    print(max(4, 6))
    print(min(4, 6))
    print(round(3.2))


    print(floor(3.2))
    print(ceil(3.2))
    print(sqrt(36))


# ----------------------------
# User Input Demo
# ----------------------------

def greet_user():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    print("Hello " + name + "! You are " + age)


# ----------------------------
# Basic Calculator
# ----------------------------

def calculator():
    num1 = input("Enter a number: ")
    num2 = input("Enter another number: ")
    result = float(num1) + float(num2)
    print(result)

#int deosnt support decimal number
#float support decimal no.
    
# ----------------------------
# Mad Libs Game
# ----------------------------

def Mad_Libs_Game():


    color = input("Enter a color: ")
    plural_noun = input("Enter a Plural Noun: ")
    celebrity = input("Enter a celebrity")

    print("Roses are " + color)
    print(plural_noun + " are blue")
    print("I love " + celebrity)

# ----------------------------
# Lists
# ----------------------------

def Lists():

    friends = ["Kevin", "Karen", "Jim", "Oscar", "Toby"]
    friends[1] = "Mike"    # Changes from Karen to Mike.
    print(friends)         # Prints the entire list
    print(friends[0])      # Prints "Kevin"
    print(friends[1:])     # Prints from index 1 to the end: ["Karen", "Jim"]
    print(fripyends[1:3])    # Prints from index 1 up to (but not including) index 3: ["Karen", "Jim"]
    
# ----------------------------
# List Functions
# ----------------------------

def List_Functions():

    lucky_numbers = [4, 8, 15, 16, 23, 42]
    friends = ["Kevin", "Karen", "Jim", "Jim", "Oscar", "Toby"]
    friends.extend(lucky_numbers)
    friends.append("Creed")  # Adds "Creed" to the end of the list
    friends.insert(1, "Kelly")  # Inserts "Kelly" at index 1
    friends.remove("Jim")  # Removes "Jim" from the list
    friends.clear()  # Clears the entire list
    friends.pop()  # Removes the last element from the list
    print(friends.index("Oscar"))  # Prints the index of "Kevin"
    print(friends.count("Jim"))  # Counts how many times "Jim" appears in the list
    friends.sort()  # Sorts the list in alphabetical order
    lucky_numbers.sort()  # Sorts the lucky numbers in ascending order
    lucky_numbers.reverse()  # Reverses the order of the lucky numbers
    friends.reverse()  # Reverses the order of the friends list
    friends2 = friends.copy()  # Creates a copy of the friends list

    print(friends2)  # Prints the copied list
    print(lucky_numbers) 
    print(friends)

# ----------------------------
# Tuples Functions
# ----------------------------

def Tuples():

    coordinates = (4, 5)
    print(coordinates[0])  # Prints the first element of the tuple
    print(coordinates[1])  # Prints the second element of the tuple

    # Tuples are immutable, so you cannot change their values
    # coordinates[0] = 10  # This will raise an error

    coordinates2 = [(4, 5), (6, 7), (80, 34)]
    print(coordinates2[0])  # Prints the first tuple in the list of tuples
    print(coordinates2[0][1])  # Prints the second element of the first tuple
    print(coordinates2[1][0])  # Prints the first element of the second tuple



# ----------------------------
# Tuples Functions
# ----------------------------



if __name__ == "__main__":
    Tuples()
