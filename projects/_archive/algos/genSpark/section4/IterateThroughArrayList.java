import java.util.*;

public class IterateThroughArrayList {
    public static ArrayList<Integer> solution(ArrayList<String> myList) {

        ArrayList<Integer> output = new ArrayList();

        for (int i = 0; i < myList.size(); i++) {
            output.add(myList.get(i).length());
        }

        return output;
    }

    public static void main(String[] args) {
        ArrayList<String> test = new ArrayList<>();
        test.add("this??");
        test.add("is??");
        test.add("a??");
        test.add("test??");
        test.add("right??????");

        System.out.println(solution(test));
    }

}
