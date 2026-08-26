public class CounterForLoop {
    public static String solution(int count) {
        String output = "";
        for (int x = count; x >= 0; x--) {
            output = output + String.valueOf(x) + " ";
        }
        return output;
    }

    public static void main(String[] args) {
        System.out.println(solution(10));
    }
}
