package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.*;


public class RemoveDuplicatesFromArray implements Assignment {
    public int[] solution(int[] nums) {

        if (nums.length == 0 || nums.length == 1) return nums;


        // get item frequencies FIRST ATTEMPT THAT ALSO GETS FREQUENCIES OF OCCURANCE
        //tried to return HashMap.keySet()
//        HashMap<Integer, Integer> no_dupes = new HashMap<Integer, Integer>();
//        for(int x = 0 ; x < nums.length; x++)
//        {
//            if (no_dupes.containsKey(nums[x]))
//            {
//                no_dupes.replace(  nums[x]  , no_dupes.get(nums[x])+ 1   )  ;
//            }
//            else {
//                no_dupes.put( nums[x]  ,  1 )  ;
//            }
//        }

        // get item frequencies
        List<Integer> output_list = new ArrayList<Integer>();
        for(int x = 0 ; x < nums.length; x++)
        {
            if( output_list.size() > 0 )
            {
                if(output_list.contains( nums[x] ))
                {
                    System.out.println("!!!!!!!!!!!!!!!!!!!!!!!");
                }
                else
                {
                    output_list.add(  nums[x]  ) ;
                }
            }
            else
            {
                output_list.add(  nums[x]  ) ;
            }
        }



        if (output_list.size() == 0 || output_list.size() == 1)
            return nums;

        int[] output_array = new int[output_list.size()];
        for(int i = 0; i < output_list.size(); i++ )
        {
            output_array[i] = output_list.get(i);
        }







        return output_array ;
    }
}
