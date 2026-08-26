public class DivideByZero {
    public static Object solution(int one, int two) {
        try {
            return one / two;
        } catch (ArithmeticException e) {
            return "Caught Exception: Divide by zero";
        }
    }

    public static void main(String[] args) {
        System.out.println(solution(1, 0));
        System.out.println(solution(10, 5));
    }

}
