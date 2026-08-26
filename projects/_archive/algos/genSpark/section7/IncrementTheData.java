package genspark.assignments.section7;

import genspark.assignments.Assignment;
import java.util.ArrayList;
import java.util.stream.Collectors;

public class IncrementTheData implements Assignment {
    public Object solution(ArrayList<Integer> nums) {
        return nums.stream()
                .map( i -> i+10   )
                .collect(Collectors.toList());
    }
}
