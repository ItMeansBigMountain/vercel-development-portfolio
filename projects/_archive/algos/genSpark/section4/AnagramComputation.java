import java.util.ArrayList;

public class AnagramComputation {
    public static boolean solution(String word1, String word2) {
        // ERROR CHECKS
        if (word1.length() != word2.length())
            return false;
        if (word1.equals(word2))
            return false;

        // INIT POP LIST
        ArrayList<Character> letter_list = new ArrayList<Character>();
        for (int x = 0; x < word1.length(); x++) {
            letter_list.add(word1.charAt(x));
        }

        // ANALYSIS POP STACK METHOD
        for (int x = 0; x < word2.length(); x++) {
            for (int y = 0; y < letter_list.size(); y++) {
                if (letter_list.get(y) == word2.charAt(x)) {
                    letter_list.remove(y);
                    break;
                }
            }
        }

        if (letter_list.size() == 0)
            return true;
        return false;
    }

    public static void main(String[] args) {
        System.out.println(solution("cinema", "iceman"));
        System.out.println(solution("java", "code"));
    }

}