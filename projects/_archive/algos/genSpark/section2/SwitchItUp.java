public class SwitchItUp {
    public static String solution(int x) {
        switch (x) {
            case 1:
                return "one";
            case 2:
                return "two";
            case 3:
                return "three";
            case 4:
                return "four";
            case 5:
                return "five";
            default:
                return "none matched";
        }
    }

    public static void main(String[] args) {
        for (var x = 0; x < 6; x++) {
            System.out.println(solution(x));
        }
    }

}
