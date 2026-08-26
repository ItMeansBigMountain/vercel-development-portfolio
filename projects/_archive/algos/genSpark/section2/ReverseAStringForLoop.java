
public class ReverseAStringForLoop {
    public static String solution(String str) {
        if (str.length() == 0)
            return "";

        String output = "";
        for (int x = str.length(); x > 0; x--) {
            output = output + str.charAt(x - 1);
        }
        return output;
    }

    public static void main(String[] args) {
        System.out.println(solution("sorry not interested"));
    }
}
