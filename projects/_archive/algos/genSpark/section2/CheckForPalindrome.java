
public class CheckForPalindrome {
    public static boolean solution(String pally) {
        if (pally.length() < 2)
            return true;

        int counter = pally.length() - 1;
        String rev = "";
        while (counter >= 0) {
            rev = rev + pally.charAt(counter);
            counter = counter - 1;
        }

        if (rev.equals(pally)) {
            return true;
        } else {
            return false;
        }

    }

    public static void main(String[] args) {
        System.out.println(solution("pally"));
        System.out.println(solution("racecar"));

    }
}
