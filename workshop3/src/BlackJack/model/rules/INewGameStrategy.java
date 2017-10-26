package BlackJack.model.rules;


import BlackJack.model.Card;
import BlackJack.model.Dealer;
import BlackJack.model.Deck;
import BlackJack.model.Player;


public interface INewGameStrategy
{
    boolean NewGame(Deck a_deck, Dealer a_dealer, Player a_player);

    /* NOTE: Static methods in interfaces only works with Java 8 and later.. */
    static void DealAndPossiblyShowCard(Deck a_deck, Player a_player,
                                        Boolean shouldShow)
    {
        Card c = a_deck.GetCard();
        c.Show(shouldShow);
        a_player.DealCard(c);
    }
}