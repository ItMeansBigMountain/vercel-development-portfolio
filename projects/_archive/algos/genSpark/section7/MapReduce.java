package genspark.assignments.section7;

import genspark.assignments.Assignment;

import java.util.ArrayList;
import java.util.Arrays;

public class MapReduce implements Assignment {
    public int[] solution(ArrayList<ArrayList<Integer>> innerNums) {


        //STREAM
        Object[] streamed_objects = innerNums.stream()
                .map(inner_list -> inner_list.stream().reduce(0, Integer::sum  ))
                .toArray();


        //CONVERT OBJECTS[] INTO INT[]
        int[] output = new int[streamed_objects.length];
        for (int i = 0; i < output.length; i++) {
            output[i] = (int) streamed_objects[i];
        }

        return output;
    }
}