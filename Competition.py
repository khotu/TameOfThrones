from pakages import Southeros, Message, MessageVerify
import Ruler
import exception
import random


class Competitors():
    ''' Class Competitors holds the functionality of competitiors class'''
    def __init__(self, competitors_string):
        """
        :param competitors_string: (string) Space seprated string of kingdoms  to be ruler
        """
        self.__competitors = competitors_string

    def competitors(self):
        """
        :return: list of kindoms
        """
        return self.__competitors.upper().split(" ")

    def is_competitor(self, kingdom):
        """

        :param kingdom:(string) name of kingdom

        :return: (bool_value) true if kingdom is a competitior itself
        """
        return kingdom in self.competitors()


   # def save_in_ballot(self,file_name, lines):
   #     with open(file_name, mode='a') as fp:
   #         fp.write("\n")
   #         fp.writelines(lines)

    def select_random_msg(self, ballot_name,no_of_message=6):
        """

        :param ballot_name: file path from where the message to be selected
        :param no_of_message: (int) number of message to be choosen randomly

        :return:list of random messages with length of no_of_message param
        """
        with open(ballot_name) as fp:
            lines = fp.readlines()
            random_messgae = random.sample(lines, k=no_of_message)
            return random_messgae

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
            raise exception.InvalidMessageException("Cannot send message to itself")

        response = MessageVerify.verify(otherKingdom, message.get_message())
        return response

    def to_be_ruler(self, competitors, southeros):
        """

        :param competitors: list of Competitiors to be ruler of Empire
        :param southeros: Southeros Class Object which hold the Registration of  all the Kingdoms of Southeros

        :return: call self.check_tie_case(number_of_allegiance, allies, southeros) function of same clss
        """
        number_of_allegiance = {}
        allies = {}
        engaged_kindoms = []
        for i, competitor in enumerate(competitors):
            ally = []
            sender_kindom = southeros.get_kingdom(competitor)
            selected_message = self.select_random_msg("message.txt")
            kingdoms = ["ICE", "WATER", "SPACE", "LAND", "AIR", "FIRE"]
            for kingdom, msg in zip(kingdoms, selected_message):
                receiver_kingdom, text = kingdom, msg
                receiver_kingdom = receiver_kingdom.upper()
                if not self.is_competitor(receiver_kingdom):
                    receiver_kingdom_object = southeros.get_kingdom(receiver_kingdom)
                    message = Message(sender_kindom, receiver_kingdom_object, text)
                    response = self.send_message(message)
                    number_of_allegiance[competitor] = number_of_allegiance.get(competitor, 0)
                    if response:
                        if receiver_kingdom not in engaged_kindoms:
                            number_of_allegiance[competitor] = number_of_allegiance.get(competitor, 0) + 1
                            ally.append(receiver_kingdom)
                            engaged_kindoms.append((receiver_kingdom))

                else:
                    # print(f"{receiver_kingdom} can not give its allince as it is itself a competitior")
                    pass
            allies[competitor] = ally
            #print(engaged_kindoms)
        print(" ===========  Result after ballot count =============")
        for key, value in number_of_allegiance.items():
            print(f"Allies for {key} :: {value}")
        return self.check_tie_case(number_of_allegiance, allies, southeros)

    def check_tie_case(self, allience_dict, allies_dict, southeros):
        """

        :param allience_dict: (dictionary) key value pair of kingdom name and number of allience,it got
        :param allies_dict: (dictionary) key value pair of kingdom name and list of its allies
        :param southeros:  Southeros Class Object which hold the Registration of  all the Kingdoms of Southeros

        """
        max_value = allience_dict[max(allience_dict, key=allience_dict.get, default= 0)]
        new_compititor = []
        for key, value in allience_dict.items():
            if value == max_value:
                new_compititor.append(key)

        if len(new_compititor) == 1:
            ruler = new_compititor[0]
            ally_of_ruler = allies_dict[ruler]
            print(f"\n\nWho is the ruler of Southeros?\n OUTPUT :: {ruler}\n Allies of Ruler? :: {ally_of_ruler}")
        else:
            print("\n\n===========================  Another Round Of Ballot  ===============================")
            self.to_be_ruler(new_compititor, southeros)

def main():
    string_ = input("Enter space seprtaed names of kindoms to be Compititiors ::   ")
    competition = Competitors(string_)
    southeros = Ruler.register_all_kingdoms()
    competitors = competition.competitors()
    competition.to_be_ruler(competitors,southeros)

if __name__ == "__main__":
    main()