public class TypeConversion {
    public static Object solution(Object object) {

        if (object instanceof String) {
            // return int
            String _s = object.toString();
            return Integer.parseInt(_s);
        }

        else {
            // return string
            return object.toString();
        }

    }

    public static void main(String[] args) {
        System.out.println(solution(5));
        System.out.println(solution("5"));
        System.out.println(solution(new int[] { 1, 2, 3 }));
    }
}
