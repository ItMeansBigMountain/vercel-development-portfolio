package genspark.assignments.section5;

import genspark.assignments.Assignment;
import java.util.Stack;

public class ParenthesisBalance implements Assignment {
    public String solution(String s) {
        if(s.isEmpty())return "unbalanced";

        Stack<Character> stack = new Stack<Character>();
        for(int i = 0; i < s.length(); i++)
        {
            if(s.charAt(i) == '(')
            {
                stack.push(s.charAt(i));
            }
            else if (s.charAt(i) == ')')
            {
                if(stack.isEmpty()) return "unbalanced";
                char latest = stack.peek();
                if(latest == '(') stack.pop();
            }
        }

        if(stack.isEmpty()) return "balanced";
        else return "unbalanced";
    }
}
