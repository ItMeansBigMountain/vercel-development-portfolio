
public class ParsingAnInteger {
    public static Object solution(String word) {
        try {
            return Integer.parseInt(word);
        } catch (NumberFormatException e) {
            return "Caught Exception: Number Format Exception";
        }
    }

    public static void main(String[] args) {
        System.out.println(solution("0"));
        System.out.println(solution("zero"));
    }
}
