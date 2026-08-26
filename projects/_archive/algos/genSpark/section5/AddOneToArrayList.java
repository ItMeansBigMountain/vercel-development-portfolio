package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.ArrayList;

public class AddOneToArrayList implements Assignment {
    public ArrayList<Integer> solution(ArrayList<Integer> list) {

        String number_string = "";
        for(int i = 0 ; i < list.size(); i++)
        {
            number_string += list.get(i);
        }

        //convert to int
        //add one
        int number_int = Integer.parseInt(number_string) + 1;

        //convert to string
        number_string = String.valueOf(number_int);


        //create list and populate list with forloop....
        list.clear();

        for(int i = 0 ; i < number_string.length(); i++)
        {
           list.add( Integer.parseInt(  String.valueOf(number_string.charAt(i) )   )     );
        }


        return list;


//        for(int i = list.size()-1 ; i > 0; i--  )
//        {
//
//            if(list.get(i) + 1 > 9  )
//            {
//                list.set( i , 0   );
//                list.set( i-1 , list.get(i-1) + 1   );
//            }
//            else
//            {
//                list.set( i , list.get(i) + 1   );
//
//            }
//
//        }





    }
}
