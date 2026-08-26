import java.util.Stack;

public class algo {

    public static boolean isValid(String s) {

        Stack<Character> st = new Stack<>();

        for (int i = 0; i < s.length(); i++) {
            char current = s.charAt(i);

            // opened then push to stack
            if (current == '(' || current == '{' || current == '[') {
                st.push(current);
            }

            // closed are specified and referenced by stack
            // check if all brackets have pairs by adding them to stack from above then
            // removing them as we find closing brackets...!
            else if (current == ')') {
                if (st.size() == 0) {
                    return false;
                } else if (st.peek() != '(') {
                    return false;
                } else {
                    st.pop();
                }
            } else if (current == '}') {
                if (st.size() == 0) {
                    return false;
                } else if (st.peek() != '{') {
                    return false;
                } else {
                    st.pop();
                }
            } else if (current == ']') {
                if (st.size() == 0) {
                    return false;
                } else if (st.peek() != '[') {
                    return false;
                } else {
                    st.pop();
                }
            }

        }

        // after calculation.... check if all symbols have popped out of stack.
        // st.size() == 0 means all have popped...
        if (st.size() == 0) {
            return true;
        } else {
            return false;
        }

    }

    public static void main(String[] args) {

        System.out.print(isValid("([])()"));

    }

}
