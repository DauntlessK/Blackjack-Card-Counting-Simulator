def simulation(gamesToSim, numDecks, reshuf):
    """Simulate x number of games with y number of decks
    counts # of wins if 'player' stays at 2 cards, or hits once"""

    head_row = ["Hand Starting Value", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "TOTAL"]
    twocard_winValues = ["Two Card Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_wins = 0
    twocard_lossValues = ["Two Card Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_losses = 0
    twocard_tieValues = ["Two Card Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_ties = 0
    threecard_winValues = ["Three Card Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_wins = 0
    threecard_lossValues = ["Three Card Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_losses = 0
    threecard_tieValues = ["Three Card Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_ties = 0
    secondHand_winValues = ["Second Hand Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_wins = 0
    secondHand_lossValues = ["Second Hand Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_losses = 0
    secondHand_tieValues = ["Second Hand Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_ties = 0
    deck = Deck(numDecks, reshuf)
    moneyTwoCard = 0     #starting money for two card
    moneyThreeCard = 0   #starting money for three card
    moneySecondHand = 0  #starting money for second hand (that hits/stands according to table)


    loops = 0
    while loops < gamesToSim:
        betAmount = getBetAmount(deck)
        myHand = Hand(betAmount, False)
        dealer = Hand(betAmount, True)
        myHand.discardHand()      # ensures hand values are empty / reset
        dealer.discardHand()      # ensures dealer hand values are empty / reset

        myHand.newHand(deck, 2)
        myHand2 = Hand(betAmount, False)
        myHand2.hand = myHand.hand
        myHand2.total = myHand.total
        myHand2.numOfAces = myHand.numOfAces
        myHand2.numOfAcesAs1 = myHand.numOfAcesAs1
        dealer.newHand(deck, 1)
        handStartingValue = myHand.getTotal()

        while getHitorStand(myHand2, dealer) == "Hit" and myHand2.getTotal() < 21 :
            myHand2.draw1(deck)

        while dealer.getTotal() <= 16:
            dealer.draw1(deck)


        #check if player1 won/lost/tied with 2 cards
        if (myHand.isBJ()):
            twocard_winValues[handStartingValue] += 1
            twocard_wins += 1
            moneyTwoCard = moneyTwoCard + getBlackJackAmount(myHand.betAmount)
        elif (dealer.isBust()) or (myHand.getTotal() > dealer.getTotal()):
            twocard_winValues[handStartingValue] += 1
            twocard_wins += 1
            moneyTwoCard = moneyTwoCard + myHand.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            twocard_tieValues[handStartingValue] += 1
            twocard_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            twocard_lossValues[handStartingValue] += 1
            twocard_losses += 1
            moneyTwoCard = moneyTwoCard - myHand.betAmount
        else:
            print("Error")

        #if hand2 did take a card, add third card to first hand so that the hands first 3 cards match
        if len(myHand2.hand) > 2:
            myHand.hand.append(myHand2.hand[2])
        else:
            myHand.draw1(deck)

        # check if player won/lost/tied with 3 cards
        if (myHand.isBust()):            #no matter what if player busts, it is a loss
            threecard_lossValues[handStartingValue] += 1
            threecard_losses += 1
            moneyThreeCard = moneyThreeCard - myHand.betAmount
        elif myHand.getTotal() > dealer.getTotal():
            threecard_winValues[handStartingValue] += 1
            threecard_wins += 1
            moneyThreeCard = moneyThreeCard + myHand.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            threecard_tieValues[handStartingValue] += 1
            threecard_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            threecard_lossValues[handStartingValue] += 1
            threecard_losses += 1
            moneyThreeCard = moneyThreeCard - myHand.betAmount
        else:
             print("Error")

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
    del twocard_winValues[1:4]
    del twocard_lossValues[1:4]
    del twocard_tieValues[1:4]
    del threecard_winValues[1:4]
    del threecard_lossValues[1:4]
    del threecard_tieValues[1:4]
    del secondHand_winValues[1:4]
    del secondHand_lossValues[1:4]
    del secondHand_tieValues[1:4]

    #add the total for each list to the final cell
    twocard_winValues.append(twocard_wins)
    twocard_lossValues.append(twocard_losses)
    twocard_tieValues.append(twocard_ties)
    threecard_winValues.append(threecard_wins)
    threecard_lossValues.append(threecard_losses)
    threecard_tieValues.append(threecard_ties)
    secondHand_winValues.append(secondHand_wins)
    secondHand_lossValues.append(secondHand_losses)
    secondHand_tieValues.append(secondHand_ties)

    #create betting info row
    betRow = ["Final money for two card bets:", moneyTwoCard,"","Final money for three card bets:", moneyThreeCard,
              "", "Final money for table bets:", moneySecondHand]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerows([head_row])
        writer.writerows([twocard_winValues])
        writer.writerows([twocard_lossValues])
        writer.writerows([twocard_tieValues])
        writer.writerows([threecard_winValues])
        writer.writerows([threecard_lossValues])
        writer.writerows([threecard_tieValues])
        writer.writerows([secondHand_winValues])
        writer.writerows([secondHand_lossValues])
        writer.writerows([secondHand_tieValues])
        writer.writerows([betRow])