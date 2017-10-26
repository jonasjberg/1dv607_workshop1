package BlackJack.model.rules;


public class RulesFactory
{

    public IHitStrategy GetHitRule()
    {
        // return new BasicHitStrategy();
        return new Soft17HitStrategy();
    }

    public INewGameStrategy GetNewGameRule()
    {
        return new AmericanNewGameStrategy();
    }

    public IWinStrategy GetWinRule()
    {
        // return new WinStrategyBasic();
        return new WinStrategyPlayerWinsIfTied();
    }
}