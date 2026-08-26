package genspark.assignments.section7;

import genspark.assignments.Assignment;
import java.util.ArrayList;

public class RemoveTheOddBalls implements Assignment {
    public Object[] solution(ArrayList<String> words) {

        return  words.stream().filter( w -> w.length() % 2 == 0 ).toArray();
    }
}
