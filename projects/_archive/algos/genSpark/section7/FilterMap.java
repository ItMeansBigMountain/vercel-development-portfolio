package genspark.assignments.section7;

import genspark.assignments.Assignment;
import java.util.ArrayList;
import java.util.stream.Collectors;

public class FilterMap implements Assignment {
    public Object[] solution(ArrayList<ArrayList<Integer>> listolists) {

        return listolists.stream()                                                                                      //makes immutable copy of steamed element
                .filter( (l) ->  l.size() % 2 == 1 )                                                                    // FILTER:  if it returns true it will retain element
                .map( odd_sized_list ->  odd_sized_list.stream().map( i -> i*10 ).collect(Collectors.toList())   )      // MAP:     lambda expression applying to every element
                .toArray();                                                                                             // converting stream into data type
    }
}
