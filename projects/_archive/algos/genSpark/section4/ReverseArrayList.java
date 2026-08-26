import java.util.ArrayList;

public class ReverseArrayList {
    public static ArrayList<Integer> solution(ArrayList<Integer> list) {

        if (list.size() == 0)
            return list;

        ArrayList<Integer> output = new ArrayList<Integer>();
        for (int x = list.size(); x > 0; x--) {
            output.add(list.get(x - 1));
        }
        return output;
    }

    public static void main(String[] args) {
        ArrayList<Integer> test = new ArrayList<>();
        test.add(1);
        test.add(2);
        test.add(3);
        test.add(4);
        test.add(5);
        test.add(6);
        test.add(7);
        test.add(8);
        test.add(9);
        test.add(10);

        System.out.println(solution(test));
    }

}
