package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.HashSet;

public class SetContainsLetter implements Assignment {
    public Object solution(HashSet<Integer> nums, int elm) {
        return nums.contains(elm) ? elm : "?" ;
    }
}
