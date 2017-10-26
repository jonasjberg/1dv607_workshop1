package BlackJack.model.rules;


import BlackJack.model.Player;


/**
 * Created by Jonas Sjöberg (js224eh) on 2017-10-26.
 */
public interface IWinStrategy
{
    boolean DealerWon(Player a_player, Player a_dealer);
}
