
public class LongestString {
    public static String solution(String firstWord, String secondWord) {
        // ↓↓↓↓ your code goes here ↓↓↓↓
        int firstLength = firstWord.length();
        int secondLength = secondWord.length();
        return firstLength > secondLength ? firstWord : secondWord;
    }

    public static void main(String[] args) {
        System.out.println(solution("Affan", "Fareed"));
    }
}
