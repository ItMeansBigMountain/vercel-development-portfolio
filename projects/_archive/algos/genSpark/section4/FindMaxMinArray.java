import java.util.ArrayList;

public class FindMaxMinArray {
    public static ArrayList<Long> solution(int[] nums) {
        ArrayList<Long> output = new ArrayList<Long>(2);

        // if empty array
        if (nums.length == 0) {
            output.add(0L);
            output.add(0L);
            return output;
        }

        // find min and max
        int minimum = nums[0];
        int maximum = nums[0];
        for (int x = 1; x < nums.length; x++) {
            if (minimum > nums[x]) { // min
                minimum = nums[x];
            }
            if (maximum < nums[x]) { // max
                maximum = nums[x];
            }
        }

        // output
        output.add((long) maximum);
        output.add((long) minimum);
        return output;

    }

    public static void main(String[] args) {
        System.out.println(solution(new int[] { 5, 9, 10, 6, 7, 3 }));
    }
}
