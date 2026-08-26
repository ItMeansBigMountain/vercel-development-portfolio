public class ReverseAnInteger {
    public static String solution(int number) {
        String num = String.valueOf(number);
        String output = "";
        for (int x = num.length() - 1; x >= 0; x--) {
            output = output + num.charAt(x);
        }
        return output;
    }

    public static void main(String[] args) {
        System.out.println(solution(123));
    }
}
