public class ArrayContainsNumber {
    public static boolean solution(int[] nums, int num) {
        for (int x = 0; x < nums.length; x++) {
            if (nums[x] == num)
                return true;
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(solution(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }, 50));
        System.out.println(solution(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }, 1));
    }
}
