package BlackJack.view;


public interface IView
{
    enum Event
    {
        HIT,
        NONE,
        PLAY,
        QUIT,
        STAND
    }

    void DisplayWelcomeMessage();

    int GetInput();

    void DisplayCard(BlackJack.model.Card a_card);

    void DisplayPlayerHand(Iterable<BlackJack.model.Card> a_hand, int a_score);

    void DisplayDealerHand(Iterable<BlackJack.model.Card> a_hand, int a_score);

    void DisplayGameOver(boolean a_dealerIsWinner);

    Event GetEvent();
}