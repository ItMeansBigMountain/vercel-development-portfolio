package genspark.assignments.section5;

import genspark.assignments.Assignment;
import it.unimi.dsi.fastutil.Hash;

import java.util.ArrayList;
import java.util.HashMap;


public class CountDuplicatesWithMap implements Assignment {
    public HashMap<Integer,Integer> solution(ArrayList<Integer> nums) {
        HashMap<Integer,Integer> hash_map = new HashMap<Integer,Integer>();

        int count = 0;
        for(int i = 0; i < nums.size(); i++)
        {
            if (  hash_map.containsKey(nums.get(i))  )
            {
                hash_map.put( nums.get(i) , hash_map.get( nums.get(i)  ) + 1);
            }
            else
            {
                hash_map.put(nums.get(i), 1  );
            }


        }



        return hash_map;
    }
}
