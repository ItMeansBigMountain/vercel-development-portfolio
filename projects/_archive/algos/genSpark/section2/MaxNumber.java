
public class MaxNumber {
    public static int solution(int a, int b) {
        // ↓↓↓↓ your code goes here ↓↓↓↓
        if (a > b)
            return a;
        else if (b > a)
            return b;
        else
            return a;
    }

    public static void main(String[] args) {
        System.out.println(solution(50, 100));
    }
}
