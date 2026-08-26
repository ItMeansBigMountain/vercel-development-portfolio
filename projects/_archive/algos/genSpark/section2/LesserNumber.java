
public class LesserNumber   {
    public static int solution(int x, int y) {
        // ↓↓↓↓ your code goes here ↓↓↓↓
        if (x < y)
            return x;
        else if (y < x)
            return y;
        else
            return x;
    }


    public static void main(String[] args) {
        System.out.println(solution(10, 100));
    }
}
