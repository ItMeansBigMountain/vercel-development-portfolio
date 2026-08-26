public class IndexOutBounds {
    public static Object solution(int[] array, int index) {
        // ↓↓↓↓ your code goes here ↓↓↓↓
        try {
            return array[index];
        } catch (ArrayIndexOutOfBoundsException e) {
            return "Caught Exception: Index Out of Bounds.";
        }
    }

    public static void main(String[] args) {
        System.out.println(solution(new int[] { 5, 10, 15, 20 }, 4));
    }
}
