def simulation2(gamesToSim, numDecks, reshuf):
    """Simulate x number of games with y number of decks
    counts # of wins if 'player' stays at 2 cards, or hits once"""

    head_row = ["Hand Starting Value", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "TOTAL"]
    secondHand_winValues = ["Second Hand Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_wins = 0
    secondHand_lossValues = ["Second Hand Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_losses = 0
    secondHand_tieValues = ["Second Hand Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_ties = 0
    deck = Deck(numDecks, reshuf)
    moneySecondHand = 0  #starting money for second hand (that hits/stands according to table)


    loops = 0
    while loops < gamesToSim:
        betAmount = getBetAmount(deck)
        myHand = Hand(betAmount, False)   #REMOVE
        dealer = Hand(betAmount, True)

        myHand2.discardHand()      # ensures hand values are empty / reset
        dealer.discardHand()      # ensures dealer hand values are empty / reset

        myHand2 = Hand(betAmount, False)
        myHand2.newHand(deck, 2)
        dealer.newHand(deck, 1)
        handStartingValue = myHand2.getTotal()

        while getHitorStand(myHand2, dealer) == "Hit" and myHand2.getTotal() < 21:
            myHand2.draw1(deck)

        while dealer.getTotal() <= 16:
            dealer.draw1(deck)

        # check if player's second hand won/lost/tied
        if (myHand2.isBust()):  # no matter what if player busts, it is a loss
            secondHand_lossValues[handStartingValue] += 1
            secondHand_losses += 1
            moneySecondHand = moneySecondHand - myHand2.betAmount
        elif myHand.getTotal() > dealer.getTotal():
            secondHand_winValues[handStartingValue] += 1
            secondHand_wins += 1
            moneySecondHand = moneySecondHand + myHand2.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            secondHand_tieValues[handStartingValue] += 1
            secondHand_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            secondHand_lossValues[handStartingValue] += 1
            secondHand_losses += 1
            moneySecondHand = moneySecondHand - myHand.betAmount
        else:
            print("Error")

        if deck.needsReshuf:
            deck.reshuf()
        loops += 1

    #remove all 0-3 results from the lists
    del secondHand_winValues[1:4]
    del secondHand_lossValues[1:4]
    del secondHand_tieValues[1:4]

    #add the total for each list to the final cell
    secondHand_winValues.append(secondHand_wins)
    secondHand_lossValues.append(secondHand_losses)
    secondHand_tieValues.append(secondHand_ties)

    #create betting info row
    betRow = ["Final money for table bets:", moneySecondHand]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerows([head_row])
        writer.writerows([secondHand_winValues])
        writer.writerows([secondHand_lossValues])
        writer.writerows([secondHand_tieValues])
        writer.writerows([betRow])