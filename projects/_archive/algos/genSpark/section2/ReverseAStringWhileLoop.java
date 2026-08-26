public class ReverseAStringWhileLoop {
    public static String solution(String str) {
        int counter = str.length() - 1;
        String output = "";
        while (counter >= 0) {
            output = output + str.charAt(counter);
            counter = counter - 1;
        }

        return output;

    }

    public static void main(String[] args) {
        System.out.println(solution("please stop calling this number"));
    }
}
