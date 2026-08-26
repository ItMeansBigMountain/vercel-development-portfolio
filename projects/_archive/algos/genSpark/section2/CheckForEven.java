
class CheckForEven {
    public static String solution(int number) {
        return number % 2 == 0 ? "even" : "odd";
    }

    public static void main(String[] args) {

        for (int i = 0; i < 10; i++) {
            System.out.println(String.format("%d : %s", i, solution(i)));
        }

    }

}
