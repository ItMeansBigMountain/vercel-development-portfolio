
public class FactorialComputation {
    public static int solution(int n) {

        // PYTHON CODE
        // factorial = lambda x : x * factorial(x-1) if x-1 > 0 else 1

        // FAILURE LAMBDA :(
        // int fact = (int x) -> x * fact(x-1) if (x == 1) return 1 ;
        // return fact(n);

        if (n == 1)
            return 1;
        return n * solution(n - 1);

    }

    public static void main(String[] args) {
        System.out.println(solution(1));
        System.out.println(solution(2));
        System.out.println(solution(3));
        System.out.println(solution(4));
        System.out.println(solution(5));
        System.out.println(solution(6));
        System.out.println(solution(7));
        System.out.println(solution(8));
        System.out.println(solution(9));
        System.out.println(solution(10));
    }

}
