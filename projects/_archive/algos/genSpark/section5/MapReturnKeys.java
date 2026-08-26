package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.ArrayList;
import java.util.HashMap;

public class MapReturnKeys implements Assignment {
    public ArrayList<String> solution(HashMap<String,Integer> map){
        ArrayList<String> arr = new ArrayList<String>();
        map.forEach(  (k,v) -> { arr.add(k);  } );
        return arr;
    }
}
