package BlackJack.model.rules;


import BlackJack.model.Card;
import BlackJack.model.Player;


/**
 * Created by Jonas Sjöberg (js224eh) on 2017-10-26.
 *
 * From the workshop instructions:
 *
 *  Soft 17 means that the dealer has 17 but in a combination of Ace and 6
 *  (for example Ace, two, two, two).
 *  This means that the Dealer can get another card valued at 10 but still
 *  have 17 as the value of the ace is reduced to 1.
 *
 *  Using the soft 17 rule the dealer should take another card (compared to the
 *  original rule when the dealer only takes cards on a score of 16 or lower).
 */
public class Soft17HitStrategy implements IHitStrategy
{
    private final int g_hitLimit = 17;

    @Override
    public boolean DoHit(Player a_dealer)
    {
        int dealerScore = a_dealer.CalcScore();

        if (dealerScore < g_hitLimit) {
            return true;
        }

        if (dealerScore == 17) {
            Player dummyHand = new Player();

            for (Card c : a_dealer.GetHand()) {
                if (c.GetValue() != Card.Value.Ace) {
                    dummyHand.DealCard(c);
                    break;
                }
            }

            if (dealerScore - dummyHand.CalcScore() == 11) {
                return true;
            }
        }

        return false;
    }
}
