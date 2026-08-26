import java.util.ArrayList;

public class FindMissingInteger {
    public static int solution(ArrayList<Integer> numbers) {

        if (numbers.size() == 0)
            return 0;
        else if (numbers.get(0) != 1)
            return 1;

        for (int x = 0; x < numbers.size() - 1; x++) {
            if (numbers.get(x) + 1 != numbers.get(x + 1)) {
                return numbers.get(x) + 1;
            }
        }

        return 0;

    }

    public static void main(String[] args) {
        ArrayList<Integer> test = new ArrayList<>();
        test.add(1);
        test.add(2);
        test.add(3);
        test.add(4);
        //MISSING 5
        test.add(6);
        test.add(7);
        test.add(8);
        test.add(9);
        test.add(10);

        System.out.println(solution(test));
    }
}
