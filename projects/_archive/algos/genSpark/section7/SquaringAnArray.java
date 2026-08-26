package genspark.assignments.section7;

import genspark.assignments.Assignment;

import java.util.Arrays;

public class SquaringAnArray implements Assignment {
    public int[] solution(int[] nums) {

        return Arrays.stream(nums).map( n -> n*n  ).toArray();
    }
}
