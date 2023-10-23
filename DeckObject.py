import random
from itertools import combinations
import collections


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        s = str(self.value)
        s += self.suit
        return s

    def __repr__(self):
        s = str(self.value)
        s += self.suit
        return s


class Deck:
    suits = ('s', 'c', 'h', 'd')
    values = (14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
    enum = {2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, 13: 1, 14: 0}

    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for suit in Deck.suits:
            for value in Deck.values:
                self.cards.append(Card(suit, value))
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    @staticmethod
    def combinations(deck):
        hand_size = 5
        return list(combinations(deck.cards, hand_size))




class Hand:
    def __init__(self, hole_cards):
        self.hole_cards = hole_cards  # 2 card list for texas hold'em

    @staticmethod
    def values(five_card_hand, sort_by_frequency=True):
        hand_values = [0] * len(five_card_hand)
        for i in range(len(five_card_hand)):
            hand_values[i] = five_card_hand[i].value
        if sort_by_frequency:
            # sort by frequency of a value: [10, 10, 9, 14, 14] >> [10, 10, 14, 14, 9]
            counts = collections.Counter(hand_values)
            return sorted(hand_values, key=lambda x: (counts[x], x), reverse=True)
        else:
            return hand_values

    @staticmethod
    def straight_flush(five_card_hand):
        rank_dict = {14: 1, 13: 2, 12: 3, 11: 4, 10: 5, 9: 6, 8: 7, 7: 8, 6: 9, 5: 10}
        is_flush, flush_rank = Hand.flush(five_card_hand)
        if is_flush:
            is_straight, straight_ranking, highest_card_in_straight = Hand.straight(five_card_hand)
            if is_straight:
                return True, rank_dict[highest_card_in_straight]
            else:
                return False, rank_dict[5]
        else:
            return False, rank_dict[5]

    @staticmethod
    def four_kind(five_card_hand):

        def rank_calculator(four_kind_card, kicker):
            rank_dict = {2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, 13: 1, 14: 0}
            combos_per_four_kind_card = 12  # e.g. 6666A > 6666K >....skip(66666) >....> 66662 = (12 combos/4 kind card)

            rank = combos_per_four_kind_card * rank_dict[four_kind_card]
            for value in Deck.values:
                if value == four_kind_card:
                    pass
                elif value == kicker:
                    rank += 1
                    return rank
                else:
                    rank += 1
            return rank

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            if hand_values[0] == hand_values[3]:
                four_kind_card, kicker = hand_values[0], hand_values[4]
                return True, four_kind_card, kicker
            else:
                return False, 'None', 'None'

        is_four_kind, four_kind_card, kicker = identify(five_card_hand)

        if is_four_kind:
            return is_four_kind, rank_calculator(four_kind_card, kicker)
        else:
            # return rank of worst four of a kind: 22223
            return is_four_kind, rank_calculator(2, 3)

    @staticmethod
    def full_house(five_card_hand):

        def rank_calculator(three_kind_card, two_kind_card):
            rank_dict = {2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, 13: 1, 14: 0}
            combos_per_three_kind_card = 12  # e.g. 666AA > 666KK >....skip(66666) >....> 66622 = (12 combos/3 kind card)

            rank = combos_per_three_kind_card * rank_dict[three_kind_card]
            for value in Deck.values:
                if value == three_kind_card:
                    pass
                elif value == two_kind_card:
                    rank += 1
                    return rank
                else:
                    rank += 1
            return rank

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            if hand_values[0] == hand_values[2]:
                if hand_values[3] == hand_values[4] and hand_values[3] != hand_values[2]:
                    three_kind_card, two_kind_card = hand_values[0], hand_values[3]
                    return True, three_kind_card, two_kind_card
                else:
                    return False, 'None', 'None'
            else:
                return False, 'None', 'None'

        is_full_house, three_kind, two_kind = identify(five_card_hand)

        if is_full_house:
            return is_full_house, rank_calculator(three_kind, two_kind)
        else:
            return is_full_house, rank_calculator(2, 3)

    @staticmethod
    def flush(five_card_hand):
        for suit in Deck.suits:
            counter = 0
            for i in range(len(five_card_hand)):
                if five_card_hand[i].suit == suit:
                    counter += 1
            if counter == 5:
                return Hand.high_card(five_card_hand)

        return False, 1274

    @staticmethod
    def straight(five_card_hand):

        def rank_calculator(highest_card_in_straight):
            rank_dict = {14: 1, 13: 2, 12: 3, 11: 4, 10: 5, 9: 6, 8: 7, 7: 8, 6: 9, 5: 10}
            return rank_dict[highest_card_in_straight]

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            counts = collections.Counter(hand_values)
            for x in counts:
                if counts[x] > 1:
                    return False, 'None'

            five_card_hand = sorted(five_card_hand, key=lambda x: x.value)
            if five_card_hand[4].value - five_card_hand[0].value == 4:
                highest_card_in_straight = five_card_hand[4].value
                return True, highest_card_in_straight

            # special straight case for A2345
            elif five_card_hand[0].value == 2 and five_card_hand[1].value == 3 and five_card_hand[2].value == 4 and \
                    five_card_hand[3].value == 5 and five_card_hand[4].value == 14:

                highest_card_in_straight = five_card_hand[3].value
                return True, highest_card_in_straight
            else:
                return False, 'None'

        is_straight, highest_card_in_straight = identify(five_card_hand)
        if is_straight:
            return is_straight, rank_calculator(highest_card_in_straight), highest_card_in_straight
        else:
            return is_straight, rank_calculator(5), highest_card_in_straight

    @staticmethod
    def three_kind(five_card_hand):

        def rank_calculator(three_kind_value, kicker_high, kicker_low):
            rank_dict = {2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, 13: 1, 14: 0}

            rank = 66 * rank_dict[three_kind_value]
            for i, v1 in enumerate(Deck.values[0: len(Deck.values) - 1]):  # enumerate 14-3 // exclude 2
                if v1 == three_kind_value:
                    pass
                else:
                    for v2 in Deck.values[i + 1: len(Deck.values)]:
                        if v2 == three_kind_value:
                            pass
                        elif v1 == kicker_high and v2 == kicker_low:
                            rank += 1
                            return rank
                        else:
                            rank += 1

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            if hand_values[0] == hand_values[2]:
                if hand_values[3] != hand_values[0] and hand_values[3] != hand_values[4]:
                    three_kind_value = hand_values[0]
                    if hand_values[3] > hand_values[4]:
                        kicker_high = hand_values[3]
                        kicker_low = hand_values[4]
                    else:
                        kicker_high = hand_values[4]
                        kicker_low = hand_values[3]
                    return True, three_kind_value, kicker_high, kicker_low
                return False, 'None', 'None', 'None'
            return False, 'None', 'None', 'None'

        is_three_kind, three_kind_value, kicker_high, kicker_low = identify(five_card_hand)
        if is_three_kind:
            return is_three_kind, rank_calculator(three_kind_value, kicker_high, kicker_low)
        else:
            return is_three_kind, rank_calculator(2, 4, 3)  # e.g. 22243

    @staticmethod
    def two_pair(five_card_hand):

        def ranking_calculator(first_pair, second_pair, kicker):
            first_pair_dict = {14: 0, 13: 12, 12: 11, 11: 10, 10: 9, 9: 8, 8: 7, 7: 6, 6: 5, 5: 4, 4: 3, 3: 2, 2: 1}
            ranking, value = 0, 14
            while first_pair <= value:
                ranking = ranking + 11 * first_pair_dict[value]
                value -= 1

            start_index = (len(Deck.values) + 2) - first_pair
            for i, value in enumerate(Deck.values[start_index: None]):
                ranking = ranking + 11 * i
                if value == second_pair:
                    break

            for j, value in enumerate(Deck.values):
                if value == first_pair or value == second_pair:
                    pass
                elif value == kicker:
                    ranking += 1
                    break
                else:
                    ranking += 1

            return ranking

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            if hand_values[0] == hand_values[1]:
                p1 = hand_values[0]
                if hand_values[2] == hand_values[3]:
                    if hand_values[2] != p1:
                        if hand_values[3] != hand_values[4]:
                            p2 = hand_values[3]
                            kicker = hand_values[4]
                            if p1 > p2:
                                first_pair_value = p1
                                second_pair_value = p2
                            else:
                                first_pair_value = p2
                                second_pair_value = p1

                            return True, first_pair_value, second_pair_value, kicker
                        else:
                            return False, 'None', 'None', 'None'
                    else:
                        return False, 'None', 'None', 'None'
                else:
                    return False, 'None', 'None', 'None'
            else:
                return False, 'None', 'None', 'None'

        is_two_pair, first_pair_value, second_pair_value, kicker = identify(five_card_hand)
        if is_two_pair:
            return is_two_pair, ranking_calculator(first_pair_value, second_pair_value, kicker)
        else:
            return is_two_pair, ranking_calculator(3, 2, 4)  # e.g. 33224

    @staticmethod
    def one_pair(five_card_hand):

        def rank_calculator(pair_value, kicker1, kicker2, kicker3):
            rank_dict = {2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, 13: 1, 14: 0}
            combos_per_pair = 220

            rank = combos_per_pair * rank_dict[pair_value]
            for i in range(len(Deck.values)):
                if Deck.values[i] == pair_value:
                    pass
                else:
                    for j in range(i + 1, len(Deck.values) - 1):
                        if Deck.values[j] == pair_value:
                            pass
                        else:
                            for k in range(j + 1, len(Deck.values)):
                                if Deck.values[k] == pair_value:
                                    pass
                                elif Deck.values[i] == kicker1 and Deck.values[j] == kicker2 and Deck.values[k] == kicker3:
                                    rank += 1
                                    return rank
                                else:
                                    rank += 1

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            if hand_values[0] == hand_values[1]:
                pair_value = hand_values[0]
                counts = collections.Counter(hand_values[1:None])
                for x in counts:
                    if counts[x] > 1:
                        return False, 'None', 'None', 'None', 'None'

                kicker_list = sorted(hand_values[2:None], reverse=True)
                kicker1, kicker2, kicker3 = kicker_list[0], kicker_list[1], kicker_list[2]

                return True, pair_value, kicker1, kicker2, kicker3
            else:
                return False, 'None', 'None', 'None', 'None'

        is_one_pair, pair_value, kicker1, kicker2, kicker3 = identify(five_card_hand)
        if is_one_pair:
            return is_one_pair, rank_calculator(pair_value, kicker1, kicker2, kicker3)
        else:
            return is_one_pair, rank_calculator(2, 5, 4, 3)  # e.g. 33224

    @staticmethod
    def high_card(five_card_hand):

        def rank_calculator(value_list):
            rank = 0
            for i in range(len(Deck.values) - 4):
                for j in range(i + 1, len(Deck.values) - 3):
                    for k in range(j + 1, len(Deck.values) - 2):
                        for m in range(k + 1, len(Deck.values) - 1):
                            for n in range(m + 1, len(Deck.values)):
                                if Deck.values[i] - Deck.values[n] == 4:
                                    pass
                                elif Deck.values[i] == 14 and Deck.values[j] == 5 and Deck.values[k] == 4 and Deck.values[m] == 3 and Deck.values[n] == 2:
                                    pass
                                elif Deck.values[i] == value_list[0] and Deck.values[j] == value_list[1] and Deck.values[k] == value_list[2] and Deck.values[m] == value_list[3] and Deck.values[n] == value_list[4]:
                                    rank += 1
                                    return rank
                                else:
                                    rank += 1

        def identify(five_card_hand):
            hand_values = Hand.values(five_card_hand, sort_by_frequency=True)
            counts = collections.Counter(hand_values)
            for x in counts:
                if counts[x] > 1:
                    return False, 'None'
            return True, hand_values

        is_high_card, hand_values = identify(five_card_hand)
        if is_high_card:
            return is_high_card, rank_calculator(hand_values)
        else:
            return is_high_card, rank_calculator([7, 6, 5, 4, 2])

    def best_hand(self, hand, community_cards):  # return best hand + ranking from all possible combinations
        pass

    @staticmethod
    def ranking(five_card_hand):  # ranking system
        total_rank = 0
        is_straight_flush, rank = Hand.straight_flush(five_card_hand)
        if is_straight_flush:
            return total_rank + rank
        else:
            total_rank = total_rank + rank
            is_four_kind, rank = Hand.four_kind(five_card_hand)
            if is_four_kind:
                return total_rank + rank
            else:
                total_rank = total_rank + rank
                is_full_house, rank = Hand.full_house(five_card_hand)
                if is_full_house:
                    return total_rank + rank
                else:
                    total_rank = total_rank + rank
                    is_flush, rank = Hand.flush(five_card_hand)
                    if is_flush:
                        return total_rank + rank
                    else:
                        total_rank = total_rank + rank
                        is_straight, rank, void = Hand.straight(five_card_hand)
                        if is_straight:
                            return total_rank + rank
                        else:
                            total_rank = total_rank + rank
                            is_three_kind, rank = Hand.three_kind(five_card_hand)
                            if is_three_kind:
                                return total_rank + rank
                            else:
                                total_rank = total_rank + rank
                                is_two_pair, rank = Hand.two_pair(five_card_hand)
                                if is_two_pair:
                                    return total_rank + rank
                                else:
                                    total_rank = total_rank + rank
                                    is_one_pair, rank = Hand.one_pair(five_card_hand)
                                    if is_one_pair:
                                        return total_rank + rank
                                    else:
                                        total_rank = total_rank + rank
                                        is_high_card, rank = Hand.high_card(five_card_hand)
                                        return total_rank + rank


def rankings_to_file(text_file):
    Handrank = collections.namedtuple('Handrank', ['handstr', 'rank'])
    deck = Deck()
    hands = deck.combinations(deck)
    print(len(hands))
    Handrank_list = [0] * len(hands)
    for i, hand in enumerate(hands):
        hand = sorted(hand, key=lambda x: x.value, reverse=True)
        handstring = ''
        for card in hand:
            handstring += str(card)
        Handrank_list[i] = Handrank(handstring, Hand.ranking(hand))

    Handrank_list = sorted(Handrank_list, key=lambda x: x.rank)

    with open(text_file, 'w') as f:
        for hand in Handrank_list:
            f.write(str(hand.rank) + '\t' + hand.handstr + '\n')


if __name__ == '__main__':

    c1 = Card('h', 7)
    c2 = Card('d', 7)
    c3 = Card('c', 9)
    c4 = Card('h', 4)
    c5 = Card('c', 4)
    c6 = Card('d', 10)

    #hand = Hand([c1, c2])
    #possible_combos = hand.combinations([c3, c4, c5, c6])

    test = [c1, c2, c3, c4, c5]
    print(Hand.ranking(test))
    rankings_to_file('handranks.txt')


