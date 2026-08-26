
public class IncrementWhileLoop {

    public static String solution(int from, int to) {
        if (from > to)
            return "";

        String output = String.valueOf(from);
        int counter = from + 1;
        while (counter <= to) {
            output = output + String.valueOf(counter);
            counter = counter + 1;
        }
        return output;
    }


    public static void main(String[] args) {
        System.out.println(  solution(5, 10)  );
    }
}
