import java.util.*;

public class MeanMedian {
    public static String solution(int a, int b, int c) {

        // INIT LIST
        List<Integer> nums = new ArrayList<Integer>();
        nums.add(0, a);
        nums.add(1, b);
        nums.add(2, c);

        // ITERATE OVER LIST
        int total = nums.get(0);
        for (int i = 1; i < nums.size(); i++) {
            total = total + nums.get(i);
            if (nums.get(i - 1) > nums.get(i)) {
                Collections.swap(nums, i - 1, i);
                for (int y = i - 1; y > 0; y--) {
                    if (nums.get(y - 1) > nums.get(y)) {
                        Collections.swap(nums, y - 1, y);
                    }
                }
            }
        }

        // CALCULATE MEAN & MEDIAN
        float mean = (float) total / nums.size();
        int median = nums.get(nums.size() / 2);

        // OUTPUT
        String output = String.valueOf(mean) + " " + String.valueOf(median);
        return output;
    }

    public static void main(String[] args) {
        System.out.println(solution(5, 100, 15));
    }

}
