from exception import KingdomNotFound, InvalidAllyKingdom, InvalidMessageException

class Message:
    """Message Class to hold the details of Message Sent"""
    def __init__(self, sender, receiver, message):
        """
        Args:
            sender (Kingdom Object): Message Sender Kingdom
            receiver (Kingdom Object): Message Receiver Kingdom
            message (string): Message that to be sent
        """
        self.__sender = sender
        self.__receiver = receiver
        self.__message = message

    def get_sender(self):
        """Gets the Sender Kingdom Object of the Message
        Returns:
            Kingdom Object: Message Sender Kingdom
        """
        return self.__sender

    def get_receiver(self):
        """Gets the Receiver Kingdom Object of the Message
        Returns:
            Kingdom Object: Message Reciever Kingdom
        """
        return self.__receiver

    def get_message(self):
        """Gets the Message Text
        Returns:
            String: Message Text
        """
        return self.__message

class MessageVerify:
    """Class that verifies if the message sent results in positive or negitive reply"""
    @classmethod
    def verify(cls, prospect_kingdom, message):
        """
        Args:
            prospect_kingdom (Kingdom Object): Reciever Kingdom
            message (string): message text that is sent
        Returns:
            bool: True if the condition is fullfilled, False otherwise
        """

        message_dict = cls.__get_frequency_of_each_character(message.lower())
        chiper_emblem_name = cls.__chiper_emblem(prospect_kingdom.emblem(),
                prospect_kingdom.emblem_length())

        emblem_dict = cls.__get_frequency_of_each_character(chiper_emblem_name.lower())

        #print(f"message dict :: {message_dict} \nemblem dict :: {emblem_dict}\n\n")
        for key in emblem_dict.keys():
            message_key_count = message_dict.get(key, 0)
            #print(f"key :: {key}, count :: {message_key_count}\n")
            if message_key_count < emblem_dict[key]:
                return False
        return True

    @classmethod
    def __get_frequency_of_each_character(cls, text):
        """Returns the frequency of each character in the given string"""
        freq = {}
        for key in text:
            freq[key] = freq.get(key, 0) + 1
        return freq

    @classmethod
    def __chiper_emblem(cls, text, chiper_key):
        """Chiper the emblem text based on the length of the emblem"""
        chiper_word = ""
        #print("---------",text)
        for char in text:
            #if char >= 'A' and char <= 'Z':
             #   newChar = chr(((ord(char) - 65 + chiper_key)%26)+65)
                chiper_word += char
            #else:
              #  chiper_word += char
        #print(">>>>>>",chiper_word)
        return chiper_word

class Kingdom:
    """Class Kindom, holds all the details of a Kingdom in Southeros"""

    __kingdoms = dict()  # static variable to hold the list of all the kingdoms of Southeros

    def __init__(self, name, emblem):
        """
        Args:
            name (string): The first parameter. Name of the Kingdom
            emblem (string): The second parameter. Emblem of the Kingdom.
        """
        self.__kingdom_name = name
        self.__kingdom_emblem = emblem
        self.__ally_kingdoms = []
        Kingdom.__add_kingdom(self)

    @classmethod
    def get_kingdom(cls, name):
        """Class Method to get Kingdom Object from Name of Kingdom
        Args:
            name (string): name of the Kingdom

        Returns:
            Kingdom Object: Kingdom Object for the given name
        Raises:
            KingdomNotFound:
                If no Kingdom is found for the kingdom name passed in as a parameter.
        """
        if name in cls.__kingdoms.keys():
            return cls.__kingdoms[name]
        else:
            raise KingdomNotFound

    @classmethod
    def __add_kingdom(cls, kingdom):
        """Class Method to add Kingdom Object to the list of Kingdoms
        Args:
            kingdom (object): Kingdom Object to be added
        """
        cls.__kingdoms[kingdom.name()] = kingdom

    def get_allies(self):
        """Returns the list of Allies the Kingdom has
        Returns:
            list: The name of all kingdoms which are allies to the Kingdom
        """
        allies = []
        for kingdom in self.__ally_kingdoms:
            allies.append(kingdom.name())
        return allies

    def name(self):
        """Get the name of the kingdom
        Returns:
            string: Name of the Kingdom
        """
        return self.__kingdom_name

    def emblem(self):
        """Get the emblem of the kingdom
        Returns:
            string: Emblem of the Kingdom
        """
        return self.__kingdom_emblem

    def emblem_length(self):
        """Get the length of emblem of the kingdom
        Returns:
            int: Size of the Emblem of Kingdom
        """
        return len(self.emblem())

    def add_ally(self, otherKingdom):
        """Adds the passed kingdom ally of the caller Kingdom
        Args:
            otherKingdom (Object): Kindom object to be ally
        Raises:
            InvalidAllyKingdom: If the to be Ally Kingdom is not valid for making Ally
        """
        if otherKingdom.name() == None:
            raise KingdomNotFound
        elif otherKingdom == self:
            raise InvalidAllyKingdom("Cannot add itself as ally")
        else:
            if not self.is_ally(otherKingdom):
                self.__ally_kingdoms.append(otherKingdom)
                otherKingdom.add_ally(self)

    def is_ally(self, otherKingdom):
        """Checks if the passed Kingdom is ally of the Caller Kingdom

        Args:
            otherKingdom (object): Kingdom to be checked
        Returns:
            bool: True if is an Ally, False otherwise.
        """
        return otherKingdom in self.__ally_kingdoms

    def total_allies(self):
        """Return the total count of Allies a Kingdom has

        Returns:
            int: Count of Allies
        """
        return len(self.__ally_kingdoms)

    def send_message(self, message):
        """Sends Message to Other Kingdom. If the message response if True,
                Adds the both sender and reciever Kingdoms as Allies

        Args:
            message (Message Object): Message Object
        Returns:
            bool: True if the response is positive, False Otherwise
        """
        otherKingdom = message.get_receiver()
        if otherKingdom == self:
            raise InvalidMessageException("Cannot send message to itself")

        response = MessageVerify.verify(otherKingdom, message.get_message())

        if response:
            self.add_ally(otherKingdom)

        return response

    def is_ruler(self):
        """Checks if the Kingdom is a ruling Kingdom
        Returns:
            bool: True if the kingdom is a ruling Kingdom, False otherwise
        """
        return self.total_allies() >= 3

    @classmethod
    def get_all(cls):
        """Class Method to iterate over all the Kingdoms
        Yields:
            `Kingdom Object`: The Kingdom Objects one by one
        """
        for kingdom_name in cls.__kingdoms.keys():
            yield cls.__kingdoms[kingdom_name]

    @classmethod
    def get_ruler(cls):
        """Class Method to get the Ruler of all Kingdoms

        Returns:
            `Kingdom Object`: Ruler Kingdom if it exists, None Otherwise
        """
        for kingdom in cls.get_all():
            if kingdom.is_ruler():
                return kingdom
        return None

    @classmethod
    def remove_all_kingdoms(cls):
        """Removes all the Kingdoms"""
        for kingdom in cls.get_all():
            del kingdom
        cls.__kingdoms.clear()

class Southeros:
    """Class to contain the World of Southeros"""

    def __init__(self, kingdoms=[]):
        """
        Args:
            kingdoms (list of tuple of str,str): List of Kingdoms and their emblems,
                defaults to empty List
        """
        self.__rulingKingdom = None
        self.__kingdom_count = 0
        self.register_kingdoms(kingdoms)

    def register_kingdom(self, name, emblem):
        """Creates a Kingdom Class for the given kingdom name and emblem
        Args:
            name (string): Name of the Kingdom
            emblem (string): Emblem of the Kingdom
        Returns:
            Kingdom Object: Return the new kingdom object
        """
        new_kingdom = Kingdom(name, emblem)
        self.__kingdom_count += 1
        return new_kingdom

    def register_kingdoms(self, kingdoms):
        """Registers all the kingdoms
        Args:
            kingdoms (list of tuple of str,str): List of Kingdoms and their emblems
        """
        for name, emblem in kingdoms:
            self.register_kingdom(name, emblem)

    def get_kingdom(self, name):
        """Get the Kingdom Object from the Name of the kingdom
        Args:
            name (string): Name of the Kingdom
        Returns:
            Kingdom Object: Kingdom Object for the given name
        Raises:
            KingdomNotFound:
                If no Kingdom is found for the kingdom name passed in as a parameter.
        """
        return Kingdom.get_kingdom(name)

    def ruler(self):
        """Get the Ruler of Southeros
        Returns:
            Kingdom Object: Ruling Kingdom Object otherwise None
        """
        if self.__rulingKingdom == None:
            self.__rulingKingdom = self.__ruling_kingdom()
        return self.__rulingKingdom

    def __ruling_kingdom(self):
        """Get the Ruler of Southeros
        Returns:
            Kingdom Object: Ruling Kingdom Object otherwise None
        """
        return Kingdom.get_ruler()

    def get_total_kingdoms(self):
        """Return the count of Total Kingdoms in Southeros
        Returns:
            int: Total count of Kingdoms
        """
        return self.__kingdom_count

