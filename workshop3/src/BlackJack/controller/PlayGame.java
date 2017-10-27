package BlackJack.controller;


import BlackJack.model.Game;
import BlackJack.model.ICardDealtObserver;
import BlackJack.view.IView;

import static BlackJack.view.IView.*;
import static BlackJack.view.IView.Event.*;


public class PlayGame implements ICardDealtObserver
{
    private IView view;
    private Game game;

    public PlayGame(Game a_game, IView a_view)
    {
        this.game = a_game;
        this.view = a_view;
        this.game.AddSubscriberCardDealt(this);
    }

    public boolean Play()
    {
        view.DisplayWelcomeMessage();

        view.DisplayDealerHand(game.GetDealerHand(), game.GetDealerScore());
        view.DisplayPlayerHand(game.GetPlayerHand(), game.GetPlayerScore());

        if (game.IsGameOver()) {
            view.DisplayGameOver(game.IsDealerWinner());
        }

        Event event = view.GetEvent();
        switch(event) {
            case HIT:
                game.Hit();
                break;
            case PLAY:
                game.NewGame();
                break;
            case STAND:
                game.Stand();
                break;
        }

        return event != QUIT;
    }

    @Override
    public void CardDealt()
    {
        System.out.printf(".");
        Sleep();
    }

    private void Sleep()
    {
        final long SLEEP_MILLISECONDS = 750;
        try {
            Thread.sleep(SLEEP_MILLISECONDS);
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }
}
