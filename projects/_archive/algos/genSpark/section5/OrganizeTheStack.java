package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.*;

public class OrganizeTheStack implements Assignment {
    public Stack<Integer> solution(Stack<Integer> stack) {
        if (stack.size() < 2) return stack;

        ArrayList<Integer> temp = new ArrayList<Integer>();
        Stack<Integer> output_stack = new Stack<Integer>();

        int popped;
        int minimum = stack.peek();
        int maxiumum = stack.peek();
        while (output_stack.isEmpty()) {
            if (!stack.isEmpty()) {
                popped = stack.pop();
                temp.add(popped);
                // if(minimum > popped) minimum = popped;
                if (maxiumum < popped) maxiumum = popped;
            } else {
                // output_stack.push(minimum);
                // temp.remove(temp.indexOf(minimum));
                output_stack.push(maxiumum);
                temp.remove(temp.indexOf(maxiumum));
            }
        }

        Collections.sort(temp);
        // for(int i = 0; i < temp.size();i++)
        // {
        // 	output_stack.push(temp.get(i));
        // }
        for (int i = temp.size() - 1; i >= 0; i--) {
            output_stack.push(temp.get(i));
        }


        return output_stack;
    }
}
