package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.Stack;


public class ReverseStringStack implements Assignment {
    public String solution(String word) {
        if( word.length() <2 ) return word;

        Stack<Character> output_stack = new Stack<>();
        String output_string = "";

        //FILL UP STACK
        for(int i = 0; i < word.length(); i++)
        {
            output_stack.push(word.charAt(i));
        }

        //POP ELEMENTS FROM STACK AND FILL OUTPUT
        for(int i = 0; i < word.length(); i++)
        {
            output_string = output_string + output_stack.pop();
        }

        return output_string;
    }
}
