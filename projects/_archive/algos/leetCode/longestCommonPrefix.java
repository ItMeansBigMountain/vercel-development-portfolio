package finishedAlgos;
import java.util.*;

class longestCommonPrefix {

    public static String longestCommonPrefix(String[] strs) {
        if(strs.length <= 1){
            if ( strs[0].equals("")  ){return "";}
            else{
                return strs[0].substring(0, strs[0].length() );
            }
        }

        if (strs[0].equals("")){
            System.out.println("EMPTY");
            return "";
        }

        String output = "";
        int iteration_letter = 0;
        while(true)
        {
            //go through every word and check iteration letter....
            //if they all the same letter, add to output, else break
            for (int i = 0; i < strs.length-1; i++) 
            {
                Character previous = strs[strs.length-1].charAt(iteration_letter);
                Character current = strs[i].charAt(iteration_letter);
                
                if( current == previous   )
                {
                    output = output + previous;
                    iteration_letter = iteration_letter + 1;
                }
                else
                {
                    return output;
                }
            }
        }
    }

    public static void main(String[] args) {

        String[] array = {"flower","flow","flight"};
        // String[] array = {"dog","racecar","car"};
        // String[] array = {"subpar","subsequent","submerge"};
        // String[] array = {"a"};
        // String[] array = {"",""};
        System.out.println(   longestCommonPrefix(  array  )  ); 

    }

}