package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.HashMap;

public class RetrieveValueFromGivenKey implements Assignment {
    public int solution(HashMap<Integer,Integer> map, Integer value) {
        return map.getOrDefault(value, 0);
    }
}
