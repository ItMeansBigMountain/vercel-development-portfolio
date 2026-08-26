
public class TripleShotAgain {
    public static boolean solution(boolean x, boolean y, boolean z) {
        return x || y || z ? true : false;
    }

    public static void main(String[] args) {
        System.out.println(solution(false, false, false));
        System.out.println(solution(true, true, true));
        System.out.println(solution(false, false, true));
    }

}
