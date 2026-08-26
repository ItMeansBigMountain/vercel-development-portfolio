package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.HashSet; // Import the HashSet class



public class AnagramWithSets implements Assignment {
    public boolean solution(String word1, String word2) {
        if (word1.length() != word2.length() ) return  false;
        if (word1.equals(word2)) return  false;


        // INIT HASH SET
        HashSet<String> hash_set = new HashSet<String>();
        for(int i = 0; i < word1.length(); i++)
        {
            hash_set.add(String.valueOf(word1.charAt(i)));
        }


        for(int i = 0; i < word2.length(); i++)
        {
            if (!hash_set.contains( String.valueOf(word2.charAt(i))  ))
            {
                return  false;
            }
        }



        return true;
    }
}
