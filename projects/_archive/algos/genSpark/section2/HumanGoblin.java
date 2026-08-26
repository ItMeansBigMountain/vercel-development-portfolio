
public class HumanGoblin   {
    public static String solution(String str) {
        // ↓↓↓↓ your code goes here ↓↓↓↓
        if (str == "human")
        {
            return "You aRe one of us!";
        }
        else if (str == "goblin")
        {
            return "Attack the Goblin!";
        }
        return null;
    }


    public static void main(String[] args) {
        System.out.println(solution("human"));
        System.out.println(solution("goblin"));
    }
}
