public class SumTheArray {
    public static int solution(int[] numbers) {
        int total = 0;
        for (int x = 0; x < numbers.length; x++) {
            total += numbers[x];
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(solution(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }));
    }
}
