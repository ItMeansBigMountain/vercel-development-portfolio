package genspark.assignments.section7;

import genspark.assignments.Assignment;
import java.util.Arrays;

public class RemoveOddsFromArray implements Assignment {
    public int[] solution(int[] nums) {
        return Arrays.stream(nums).filter( i -> i % 2 == 0  ).toArray();
    }
}
