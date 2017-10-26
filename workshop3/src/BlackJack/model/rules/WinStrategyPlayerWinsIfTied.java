package BlackJack.model.rules;


import BlackJack.model.Player;


/**
 * Created by Jonas Sjöberg (js224eh) on 2017-10-26.
 */
public class WinStrategyPlayerWinsIfTied implements IWinStrategy
{
    private final int G_MAXSCORE = 21;

    @Override
    public boolean DealerWon(Player a_player, Player a_dealer)
    {
        int playerScore = a_player.CalcScore();
        int dealerScore = a_dealer.CalcScore();

        if (playerScore > G_MAXSCORE) {
            return true;
        } else if (dealerScore > G_MAXSCORE) {
            return false;
        }
        return dealerScore > playerScore;
    }
}
