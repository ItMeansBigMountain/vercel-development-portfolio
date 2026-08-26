package genspark.assignments.section7;

import genspark.assignments.Assignment;

import java.util.Arrays;

public class SumAnArray implements Assignment {
    public int solution(int[] nums) {
        return Arrays.stream(nums).reduce(0, (s,i) -> s+i );
    }
}
