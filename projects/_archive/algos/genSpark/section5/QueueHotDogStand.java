package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.ArrayList;
import java.util.Stack;

public class QueueHotDogStand implements Assignment {
    public ArrayList<Integer> solution(ArrayList<Integer> list) {

        if (list.size() < 2) return list;

        //POPULATE STACK
//        Stack<Integer> output_stack = new Stack<Integer>();
//        for(int x = list.size()-1; x >= 0; x--)
//        {
//            output_stack.push(list.get(x));
//        }


        //SIMULATE ROTATIONS
        int rotations = 3;
        int popped;
        for (int i = 0; i < rotations; i++) {
            popped = list.remove(0);
            list.add(popped);
        }


        return list;

    }
}
