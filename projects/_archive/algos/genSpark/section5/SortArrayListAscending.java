package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.ArrayList;
import java.util.Collections;

public class SortArrayListAscending implements Assignment {
    public ArrayList<Integer> solution(ArrayList<Integer> list) {
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i - 1) > list.get(i)) {
                Collections.swap(list, i - 1, i);
                for (int y = i - 1; y > 0; y--) {
                    if (list.get(y - 1) > list.get(y)) {
                        Collections.swap(list, y - 1, y);
                    }
                }
            }
        }
        return list;
    }
}
