
public class FirstAndLast {
    public static boolean solution(String word) {
        if (word.length() > 0)
            return word.charAt(0) == word.charAt(word.length() - 1) ? true : false;
        else
            return true;
    }

    public static void main(String[] args) {
        System.out.println(solution("testing"));
        System.out.println(solution("nathan loves python"));
    }
}
