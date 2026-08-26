package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.ArrayList;



public class EvenAfterOdds implements Assignment {
    public ArrayList<Integer> solution(ArrayList<Integer> nums) {
        if (nums.isEmpty() || nums.size() == 1) return nums;

        //PLACEMENT OF QUEUE IS AT 0 AND IF ITS ODD, placement++
        //MOVE EVERY EVEN NUMBER TO END OF LIST

        int placement = 0;
        for (int i = 0; i < nums.size() ; i++) {
            if(nums.get(placement) % 2 == 0)
            {
                int remove_and_place_at_end = nums.remove(placement);
                nums.add( remove_and_place_at_end  );
            }
            else placement++;
        }

        return nums ;
    }
}
