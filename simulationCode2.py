def simulation(gamesToSim, numDecks, reshuf):
    """Simulate x number of games with y number of decks
    and bets the same hand 3 different ways to test the best way to make money"""

    head_row = ["Hand Starting Value", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "TOTAL"]
    hand_winValues = ["Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hand_wins = 0
    hand_lossValues = ["Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hand_losses = 0
    hand_tieValues = ["Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hand_ties = 0
    deck = Deck(numDecks, reshuf)
    moneyFlatBet = 0  # starting money for flat min bet
    flatBetAmount = 5  # how much flat better bets
    moneyRandBet = 0  # starting money for random bet
    minRandBetRange = 5  # min amount for random bet
    maxRandBetRange = 20  # max amount for random bet
    moneyCardCountBet = 0  # starting money for card counting bet method

    loops = 0
    while loops < gamesToSim:
        betAmount = getBetAmount(deck)
        myHand = Hand(betAmount, False)
        dealer = Hand(betAmount, True)
        myHand.discardHand()  # ensures hand values are empty / reset
        dealer.discardHand()  # ensures dealer hand values are empty / reset

        myHand.newHand(deck, 2)
        dealer.newHand(deck, 1)
        handStartingValue = myHand.getTotal()

        while getHitorStand(myHand, dealer) == "Hit" and myHand.getTotal() < 21:
            myHand.draw1(deck)

        while dealer.getTotal() <= 16 and myHand.isNotBust():
            dealer.draw1(deck)

        # check win/loss/tie scenarios
        if (myHand.isBJ()):
            hand_winValues[handStartingValue] += 1
            hand_wins += 1

            # get payouts for blackjack and add amounts to existing totals
            moneyCardCountBet = moneyCardCountBet + getBlackJackAmount(myHand.betAmount)
            moneyFlatBet = moneyFlatBet + getBlackJackAmount(flatBetAmount)
            moneyRandBet = moneyRandBet + getBlackJackAmount(random.randint(minRandBetRange, maxRandBetRange))
        elif (myHand.getTotal() < dealer.getTotal() and dealer.isNotBust()) or myHand.isBust():
            hand_lossValues[handStartingValue] += 1
            hand_losses += 1

            # money adjustments for player being less than dealer (if dealer is not bust) or if player busted
            moneyCardCountBet = moneyCardCountBet - getBetAmount(deck)
            moneyFlatBet = moneyFlatBet - flatBetAmount
            moneyRandBet = moneyRandBet - random.randint(minRandBetRange, maxRandBetRange)
        elif (dealer.isBust()) or (myHand.getTotal() > dealer.getTotal()):
            hand_winValues[handStartingValue] += 1
            hand_wins += 1

            # money adjustments for player being less than dealer (if dealer is not bust) or if player busted
            moneyCardCountBet = moneyCardCountBet + getBetAmount(deck)
            moneyFlatBet = moneyFlatBet + flatBetAmount
            moneyRandBet = moneyRandBet + random.randint(minRandBetRange, maxRandBetRange)
        elif myHand.getTotal() == dealer.getTotal():
            hand_tieValues[handStartingValue] += 1
            hand_ties += 1
        else:
            print("Error")

        if deck.needsReshuf:
            deck.reshuf()
        loops += 1

    # remove all 0-3 results from the lists
    del hand_winValues[1:4]
    del hand_lossValues[1:4]
    del hand_tieValues[1:4]

    # add the total for each list to the final cell
    hand_winValues.append(hand_wins)
    hand_lossValues.append(hand_losses)
    hand_tieValues.append(hand_ties)

    # create betting info row
    betRow1 = ["$ for flat bet:", moneyFlatBet]
    betRow2 = ["$ for random bet:", moneyRandBet]
    betRow3 = ["$ for card count bet:", moneyCardCountBet]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerows([head_row])
        writer.writerows([hand_winValues])
        writer.writerows([hand_lossValues])
        writer.writerows([hand_tieValues])
        writer.writerows([betRow1])
        writer.writerows([betRow2])
        writer.writerows([betRow3])