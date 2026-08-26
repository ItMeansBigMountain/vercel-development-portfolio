package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.Stack;

public class DeleteMiddleOfStack implements Assignment {
    public Stack<Integer> solution(Stack<Integer> stack) {
        if (stack.empty()) return stack;

        if (stack.size() % 2 == 0) {
            int indicies = stack.size() - 1;
            int mid = indicies / 2;
            stack.remove(mid);
        } else{
            stack.remove((int) stack.size() / 2);
        }
        return stack;
    }
}



