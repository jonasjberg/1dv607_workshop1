package BlackJack.model;


import java.util.LinkedList;
import java.util.List;


public class Deck
{

    private List<Card> m_cards;

    public Deck()
    {
        m_cards = new LinkedList<Card>();

        for (int cIx = 0; cIx < Card.Color.Count.ordinal(); cIx++) {
            for (int vIx = 0; vIx < Card.Value.Count.ordinal(); vIx++) {
                Card c = new Card(Card.Color.values()[cIx],
                                  Card.Value.values()[vIx]);
                AddCard(c);
            }
        }

        Shuffle();
    }

    public void AddCard(Card a_cardToAdd)
    {
        m_cards.add(a_cardToAdd);
    }

    public Card GetCard()
    {
        Card c = m_cards.get(0);
        m_cards.remove(0);

        return c;
    }

    public Iterable<Card> GetCards()
    {
        return m_cards;
    }

    private void Shuffle()
    {
        for (int i = 0; i < 1017; i++) {
            int  index = (int) (Math.random() * 171717.0) % m_cards.size();
            Card c     = m_cards.get(index);
            m_cards.remove(index);
            AddCard(c);
        }
    }

    /**
     * Gets a card from the deck, modifies the card "shown" state and deals
     * the card to a specified player.
     *
     * @param a_player The player that the card will be dealt to.
     * @param shouldShowCard Whether the card should be shown or not.
     */
    public void DealAndPossiblyShowCard(Player a_player, Boolean shouldShowCard)
    {
        Card c = GetCard();
        c.Show(shouldShowCard);
        a_player.DealCard(c);
    }
}