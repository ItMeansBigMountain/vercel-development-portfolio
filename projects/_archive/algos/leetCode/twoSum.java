package finishedAlgos;

import java.util.*;

class algo {
    public static int[] TwoSum(int[] nums, int target) {

        for (int i = 0; i < nums.length; i++) {
            for (int x = 0; x < nums.length; x++) {
                System.out.println(nums[x]);
                System.out.println(nums[i]);
                System.out.println("-----------------");

                if (x == i) {
                    continue;
                }
                if (nums[x] + nums[i] == target) {
                    int[] output = { x, i };
                    return output;
                }

            }
        }

        int[] output = { 0 };
        return output;
    }

    public static void main(String[] args) {
        int[] array = { 1, 3, 4, 2, 1 };
        int target = 6;

        System.out.println(Arrays.toString(TwoSum(array, target)));
    }

}