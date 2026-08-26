package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.ArrayList;



public class MaxSubArray implements Assignment {

    public ArrayList<Integer> solution(ArrayList<Integer> nums) {
        if (nums.isEmpty() || nums.size() == 1) return nums;

        // FIND SEQUENCE OF NUMBERS THAT ADD UP THE MOST


        // TEMP VARIABLES TO PARSE THROUGH LIST
        int anchor = nums.size() - 1;
        int extend;

        // RUNNING TOTAL FOR EACH SUB LIST
        int total;
        ArrayList<Integer> subList = new ArrayList<Integer>();

        // MAX TOTAL FOR LIST
        int Output_total = 0;
        int max_list_start = 0;
        int max_list_end = 0;


        //ANCHOR POINT
        while (anchor >= 0) {
            //FALL BACK TO ANCHOR POINT
            extend = 0;
            for (int i = anchor; i >= 0; i--) {
                total = 0;
                //CREATE SUB LIST
                for (int y = anchor; y >= extend; y--) {
                    subList.add(nums.get(y));
                    total += nums.get(y);
                }

                //DEBUG
                System.out.print(subList);
                System.out.print("\t\t\t\t>>>>  ");
                System.out.println(total);

                //CHECK FOR MAX
                if (Output_total < total) {
                    Output_total = total;
                    max_list_start = extend;
                    max_list_end = anchor;
                }

                //RESET
                subList.clear();
                extend++;
            }
            System.out.println("---------");
            anchor--;
        }


        System.out.println(nums.subList(max_list_start, max_list_end + 1));
        System.out.println(Output_total);

        return new ArrayList<Integer>(nums.subList(max_list_start, max_list_end + 1));
    }


}

