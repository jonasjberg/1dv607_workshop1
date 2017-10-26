package BlackJack;


import BlackJack.controller.PlayGame;
import BlackJack.model.Game;
import BlackJack.view.IView;
import BlackJack.view.SimpleView;
import BlackJack.view.SwedishView;


public class Program
{

    public static void main(String[] a_args)
    {

        Game     g    = new Game();
        IView    v    = new SimpleView();
        // IView    v    = new SwedishView();
        PlayGame ctrl = new PlayGame(g, v);

        while (ctrl.Play()) {
            ;
        }
    }
}