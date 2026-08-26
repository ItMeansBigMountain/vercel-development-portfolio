package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.ArrayList;

public class FindMissingNums implements Assignment {
    public ArrayList<Integer> solution(ArrayList<Integer> nums) {

        ArrayList<Integer> missing = new ArrayList<Integer>();
        int start = 0;
        int end;

        for(int i = 0; i< nums.size(); i++)
        {
            end = nums.get(i);
            for(int j = start + 1; j < end ; j++)
            {
                missing.add( j );
            }
            start = end;
        }
        for(int x = nums.get(nums.size()-1) +1 ; x < 101; x++)
        {
            missing.add( x );
        }




        return missing;
    }
}
