package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.ArrayList;

public class LastIndexFound implements Assignment {
    public int solution(ArrayList<Integer> nums, int numToFind) {
        int output = -1;

        for(int x = nums.size() - 1 ; x >= 0; x--)
        {
            if( numToFind == nums.get(x) ) {
                output = x;
                break;
            }
        }

        return output ;
    }
}
