public class TripleShot {
    public static boolean solution(boolean x, boolean y, boolean z) {
        // ↓↓↓↓ your code goes here ↓↓↓↓
        if (x && y && z)
            return true;
        else
            return false;
    }

    public static void main(String[] args) {
        System.out.println(solution(false, false, false));
        System.out.println(solution(true, true, true));
        System.out.println(solution(false, false, true));
    }
}
