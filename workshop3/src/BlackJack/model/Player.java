package BlackJack.model;


import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;


public class Player
{

    private List<Card> m_hand;
    protected final int g_maxScore = 21;
    protected ArrayList<ICardDealtObserver> m_subscribers;

    public Player()
    {
        m_hand = new LinkedList<Card>();
        m_subscribers = new ArrayList<>();
    }

    public void DealCard(Card a_addToHand)
    {
        m_hand.add(a_addToHand);
        NotifyObserversCardDealt();
    }

    public Iterable<Card> GetHand()
    {
        return m_hand;
    }

    public void ClearHand()
    {
        m_hand.clear();
    }

    public void ShowHand()
    {
        for (Card c : m_hand) {
            c.Show(true);
        }
    }

    public int CalcScore()
    {
        // the number of scores is dependant on the number of scorable values
        // as it seems there is no way to do this check at compile time in java ?!
        // cardScores[13] = {...};
        int cardScores[] = {
                2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
        };
        assert (cardScores.length == Card.Value.Count.ordinal()) :
                "Card Scores array size does not match number of card values";


        int score = 0;

        for (Card c : GetHand()) {
            if (c.GetValue() != Card.Value.Hidden) {
                score += cardScores[c.GetValue().ordinal()];
            }
        }

        if (score > g_maxScore) {
            for (Card c : GetHand()) {
                if (c.GetValue() == Card.Value.Ace && score > g_maxScore) {
                    score -= 10;
                }
            }
        }

        return score;
    }

    public void RegisterSubscriberCardDealt(ICardDealtObserver newSubscriber)
    {
        m_subscribers.add(newSubscriber);
    }

    public void NotifyObserversCardDealt()
    {
        for (ICardDealtObserver s : m_subscribers) {
            s.CardDealt();
        }
    }
}
