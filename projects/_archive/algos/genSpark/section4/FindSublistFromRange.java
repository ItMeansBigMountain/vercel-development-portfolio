import java.util.ArrayList;

public class FindSublistFromRange {
    public static ArrayList<Integer> solution(ArrayList<Integer> elms, int from, int to) {

        ArrayList<Integer> output = new ArrayList<Integer>();

        for (int x = from; x <= elms.size(); x++) {
            if (x == to)
                break;
            output.add(elms.get(x));
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

        System.out.println(solution(test, 4, 8));
    }
}
