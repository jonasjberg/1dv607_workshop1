package BlackJack.model.rules;


import BlackJack.model.Dealer;
import BlackJack.model.Deck;
import BlackJack.model.Player;


class InternationalNewGameStrategy implements INewGameStrategy
{

    public boolean NewGame(Deck a_deck, Dealer a_dealer, Player a_player)
    {
        a_deck.DealAndPossiblyShowCard(a_player, true);
        a_deck.DealAndPossiblyShowCard(a_dealer, true);
        a_deck.DealAndPossiblyShowCard(a_player, true);

        return true;
    }
}